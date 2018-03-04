#! /usr/bin/env python3
import json
import paho.mqtt.client as mqtt
from _controller import Controller
from message_types import Topics
from action_queue import ActionQueue, ActionQueueLockedException
from box_helper import mockBoxes, quantitative1
import cv2
import time
import numpy
import base64

config = json.load(open("config.json"))

controllerClient = mqtt.Client()
client11 = mqtt.Client()
#client31 = mqtt.Client()

visionTag = "vision"
controllerTag = "controller"
flag = 0

def onStartController(client, userdata, msg, controller):
    print("> Controller started...")

def onProcess(client, userdata, msg, controller):
    global flag
    flag = 1
    print("> On process called")
    controller.changeExecutionQueue(visionTag)
    visionActionQueue = controller.actionQueues[visionTag]
    quantitative1(visionActionQueue)

    currentExecThread = controller.currentExecutionThread()

def onProcessResponse(client, userdata, msg, controller):
    # should get the response from the vision system
    global flag
    flag = 0

    if msg.payload.decode() == "True":
        print("> Accepted")
    elif msg.payload.decode() == "False":
        print("> Not accepted")

def onSwitchExecutionThread(client, userdata, msg, controller):
    tag = msg.payload.decode()
    switched = controller.changeExecutionQueue(tag)
    if switched:
        print("> Execution thread switched to {0}".format(tag))
    else:
        print("> Execution thread not switched to {0}".format(tag))

def onSwitchToPending(client, userdata, msg, controller):
    tag = msg.payload.decode()
    execThread = None
    if tag == "":
        execThread = controller.currentExecutionThread()
    else:
        execThread = controller.actionQueues[tag]

    if execThread.state.waiting:
        print("Execution thread is waiting for an action to finish.")
        print("Please stop the execution thread and then switch to pending!")
        return

    execThread.state.pending = True
    print("Execution thread was switched to pending")

def onSwitchToNotPending(client, userdata, msg, controller):
    tag = msg.payload.decode()
    execThread = None
    if tag == "":
        execThread = controller.currentExecutionThread()
    else:
        execThread = controller.actionQueues[tag]

    if execThread.state.waiting:
        print("Execution thread is waiting for an action to finish.")
        print("Please stop the execution thread and then switch to not pending!")
        return

    execThread.state.pending = False
    print("Execution thread was switched to pending")

def forwardAction(action):
    def curriedForwardedAction(client, userdata, msg, controller):
        controller.changeExecutionQueue(controllerTag)
        client.publish(Topics.APP_RECIEVE_THREAD, controller.currentExecThreadTag)
        payload = msg.payload.decode()
        controller.actionQueues[controllerTag].put({
            "action": action,
            "payload": payload
        })
        currentExecThread = controller.currentExecutionThread()
        if currentExecThread.state.pending:
            client11.publish(Topics.EV3_REQUEST_NEXT)
        print("> Next action added to the queue")

    return curriedForwardedAction

def onEV3ActionCompleted(client, userdata, msg, controller):
    """The ev3 listeners is informed that ev3 has completed an action
    This will look in the state of the current execution thread and accordingly
    respond to this message

    States:
    - ["RUNNING", "WAITING", "PENDING"] => an action should be sent next
    and waiting should be removed from the states
    - ["RUNNING", "WAITING"] => waiting should be removed from the states
    - ["RUNNING", "LOCKED", "WAITING", "PENDING or not PENDING"] =>
    nothing should be performed here. the execution thread is stopped
    """
    currentExecThread = controller.currentExecutionThread()
    controller.removeFirstAction()
    if currentExecThread is None:
        print(">>> No execution thread found in the controller!")
        client.publish(Topics.APP_REQUEST, "all")
        return
    if currentExecThread.waiting():
        print(">>> Thread was waiting")
        currentExecThread.state.waiting = False
    if currentExecThread.locked():
        print(">>> Execution thread is locked. Actions can't be performed")
        client.publish(Topics.APP_REQUEST, "all")
        return
    if currentExecThread.pending():
        if not currentExecThread.empty():
            client.publish(Topics.EV3_REQUEST_NEXT)
        else:
            print("> No actions left in the execution queue")
    client.publish(Topics.APP_REQUEST, "all")

def onRequestNextEV3Action(client, userdata, msg, controller):
    """Sends the next action to the ev3's.
    It sends only if the state is RUNNING, and if the thread is waiting
    or locked it won't send any.

    States:
    - ["RUNNING", "WAITING"] => no action to be sent. thread still waiting for
    the action to stop
    - ["RUNNING", not "LOCKED"] => action can be sent
    - ["LOCKED", *] => no action. current exec thread is locked
    """
    currentExecThread = controller.currentExecutionThread()
    client.publish(Topics.APP_REQUEST, "all")
    if currentExecThread.locked():
        print("> Current execution thread is locked")
        return
    if currentExecThread.waiting():
        print("> Action is not finished on EV3. Can't perform any actions!")
        return
    if currentExecThread.running():
        if not currentExecThread.empty():
            nextAction = controller.nextAction()
            client11.publish(nextAction["action"], nextAction["payload"])
            #client31.publish(nextAction["action"], nextAction["payload"])
            currentExecThread.state.waiting = True
            print("> Next action sent to ev3")
        else:
            print("> No actions in execution thread!")
    client.publish(Topics.APP_REQUEST, "all")

def onEV3Stop(client, userdata, msg, controller):
    """This will stop execution on the ev3, and the current action performing
    will not finish!. It will stop in the current position. It only acts on the
    current execution thread
    """
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.lock()
    currentExecThread.state.waiting = False
    client11.publish(Topics.EV3_STOP)
    #client31.publish(Topics.EV3_STOP)
    print("> Action queue locked. Ev3s are STOPPED")

def onEV3Resume(client, userdata, msg, controller):
    """This will resume the execution of the current execution thread.
    """
    client11.publish(Topics.EV3_RESUME)
    #client31.publish(Topics.EV3_RESUME)
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.unlock()
    print("> Execution thread unlocked and ready to resume")
    if currentExecThread.pending():
        client11.publish(Topics.EV3_REQUEST_NEXT)

def onEV3Pause(client, userdata, msg, controller):
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.lock()
    client11.publish(Topics.EV3_PAUSE)
    #client31.publish(Topics.EV3_PAUSE)
    print("> Action queue is locked and ev3s are PAUSED")
    return

def onPrintStates(client, userdata, msg, controller):
    print("> These are the current execution threads: ")
    for tag in controller.actionQueues:
        print("{0} => {1} with actions:".format(
            tag,
            controller.actionQueues[tag].state),
            controller.actionQueues[tag])

def onPrintPositions(client, userdata, msg, controller):
    print("> These are the current positions: ")
    client11.publish(Topics.EV3_PRINT_POS)
    #client31.publish(Topics.EV3_PRINT_POS)

def onDelete(client, userdata, msg, controller):
    currentExecThread = controller.currentExecutionThread()
    payload = msg.payload.decode()
    pos = None

    if not currentExecThread.state.locked:
        print("> Current execution thread must be locked!")
        print("> Action was NOT deleted.")
        return

    if payload == "first":
        pos = 0
    elif payload == "last":
        pos = len(currentExecThread) - 1
    elif payload == "all":
        for i in range(len(currentExecThread)):
            currentExecThread.remove(0)
        print("> Deleted all actions in the queue")
        return
    else:
        # asusmed it's an integer
        pos = int(payload)

    if pos >= 0 and pos < len(currentExecThread):
        removed = currentExecThread.remove(pos)
        if removed == None:
            print("> Action was not deleted!")
        else:
            print("> Action WAS deleted.")
    else:
        print("Positional argument is not within queue boundary")
        return

def onNext(client, userdata, msg, controller):
    currentExecThread = controller.currentExecutionThread()
    if currentExecThread.state.pending:
        print("> Current exec thread is already pending")
        print("> Next action is not implemented for pending threads")
        return
    if currentExecThread.state.waiting:
        print("> Can't send next action because thread is waiting!")
        return
    if currentExecThread.state.locked:
        print("> Current exec thread is locked!")
        return
    client11.publish(Topics.EV3_REQUEST_NEXT)
    print("> Next action should be sent to ev3.")

def onAppRequestData(client, userdata, msg, controller):
    whatToSend = msg.payload.decode()
    currentExecThread = controller.currentExecutionThread()
    if whatToSend == "thread":
        client.publish(Topics.APP_RECIEVE_THREAD, controller.currentExecThreadTag)
    elif whatToSend == "locked":
        client.publish(Topics.APP_RECIEVE_LOCKED, currentExecThread.state.locked)
    elif whatToSend == "pending":
        client.publish(Topics.APP_RECIEVE_PENDING, currentExecThread.state.pending)
    elif whatToSend == "waiting":
        client.publish(Topics.APP_RECIEVE_WAITING, currentExecThread.state.waiting)
    elif whatToSend == "actions":
        actions = numpy.array(currentExecThread.queue).tolist()
        client.publish(Topics.APP_RECIEVE_ACTIONS, json.dumps(actions))
    elif whatToSend == "all":
        client.publish(Topics.APP_REQUEST, "thread")
        client.publish(Topics.APP_REQUEST, "locked")
        client.publish(Topics.APP_REQUEST, "pending")
        client.publish(Topics.APP_REQUEST, "waiting")
        client.publish(Topics.APP_REQUEST, "actions")

controller = Controller()
visionActionQueue = ActionQueue(pending=False)
controllerActionQueue = ActionQueue()

controller.addActionQueue(visionTag, visionActionQueue)
controller.addActionQueue(controllerTag, controllerActionQueue)
controller.changeExecutionQueue(visionTag)

subscribedTopics = {
    # controller related
    Topics.START_CONTROLLER: onStartController,
    Topics.PROCESS_CONTROLLER: onProcess,
    Topics.PROCESS_RESPONSE_CONTROLLER: onProcessResponse,
    Topics.SWITCH_CONTROLLER_EXEC: onSwitchExecutionThread,
    Topics.CONTROLLER_DELETE: onDelete,
    Topics.SWITCH_EXEC_PENDING: onSwitchToPending,
    Topics.SWITCH_EXEC_NOT_PENDING: onSwitchToNotPending,
    Topics.CONTROLLER_NEXT_ACTION: onNext,
    # the controller will only forwards to ev3
    Topics.CONTROLLER_MOVE_X: forwardAction(Topics.EV3_MOVE_X),
    Topics.CONTROLLER_MOVE_Y: forwardAction(Topics.EV3_MOVE_Y),
    Topics.CONTROLLER_MOVE_Z: forwardAction(Topics.EV3_MOVE_Z),
    Topics.CONTROLLER_GRAB: forwardAction(Topics.EV3_MOVE_GRAB),
    Topics.CONTROLLER_RELEASE: forwardAction(Topics.EV3_MOVE_RELEASE),
    Topics.CONTROLLER_RESET_X: forwardAction(Topics.EV3_RESET_X),
    Topics.CONTROLLER_RESET_Y: forwardAction(Topics.EV3_RESET_Y),
    Topics.CONTROLLER_RESET_Z: forwardAction(Topics.EV3_RESET_Z),
    # ev3 related
    Topics.STOP_CONTROLLER: onEV3Stop,
    Topics.PAUSE_CONTROLLER: onEV3Pause,
    Topics.RESUME_CONTROLLER: onEV3Resume,
    # client-controller related
    Topics.CONTROLLER_PRINT_STATES: onPrintStates,
    Topics.CONTROLLER_PRINT_POS: onPrintPositions,

    Topics.APP_REQUEST: onAppRequestData
}

def onConnect(client, userdata, flags, rc):
    print("Controller listening to messages")
    for key in subscribedTopics.keys():
        client.subscribe(key)
    client.publish(Topics.APP_REQUEST, "all")

def onMessage(client, userdata, msg):
    if msg.topic in subscribedTopics.keys():
        if not msg.topic == Topics.APP_REQUEST:
            client.publish(Topics.APP_REQUEST, "all")
        subscribedTopics[msg.topic](client, userdata, msg, controller)
        if not msg.topic == Topics.APP_REQUEST:
            client.publish(Topics.APP_REQUEST, "all")
    else:
        print("Topic {0} is not subscribed".format(msg.topic))

client11.connect(config["ips"]["INF_11"], 1883, 60)
#client31.connect(config["ips"]["INF_31"], 1883, 60)
controllerClient.connect(config["ips"]["CONTROLLER"], 1883, 60)

def onPrint(client, userdata, msg, controller):
    print(msg.payload.decode())

def onEV3Connect(client, userdata, flags, rc):
    client.subscribe(Topics.EV3_REQUEST_NEXT)
    client.subscribe(Topics.EV3_ACTION_COMPLETED)
    client.subscribe(Topics.CONTROLLER_PRINT)

def onEV3Message(client, userdata, msg):
    if msg.topic == Topics.EV3_REQUEST_NEXT:
        onRequestNextEV3Action(client, userdata, msg, controller)
    elif msg.topic == Topics.EV3_ACTION_COMPLETED:
        onEV3ActionCompleted(client, userdata, msg, controller)
    elif msg.topic == Topics.CONTROLLER_PRINT:
        onPrint(client, userdata, msg, controller)

client11.on_connect = onEV3Connect
#client31.on_connect = onEV3Connect
client11.on_message = onEV3Message
#client31.on_message = onEV3Message

controllerClient.on_connect = onConnect
controllerClient.on_message = onMessage

client11.loop_start()
#client31.loop_start()
controllerClient.loop_start()

while True:
    if flag == 1:
        cap = cv2.VideoCapture(0)
        while flag == 1:
            retval, img = cap.read()
            if img is not None:
                img = cv2.flip(img, 1)
                retval, buffer = cv2.imencode('.jpg', img)
                jpg = base64.b64encode(buffer)
                controllerClient.publish(Topics.APP_RECIEVE_IMG, jpg)
        cap.release()
    else:
        time.sleep(0.01)
