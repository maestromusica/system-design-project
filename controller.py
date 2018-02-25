#! /usr/bin/env python3
import json
import paho.mqtt.client as mqtt
from _controller import Controller
from message_types import Topics
from action_queue import ActionQueue, ActionQueueLockedException
from box_helper import mockBoxes

config = json.load(open("config.json"))

controllerClient = mqtt.Client()
client11 = mqtt.Client()
client31 = mqtt.Client()

visionTag = "vision"
controllerTag = "controller"

def onStartController(client, userdata, msg, controller):
    visionActionQueue = ActionQueue()
    controllerActionQueue = ActionQueue()
    # mockBoxes(visionActionQueue)

    controller.addActionQueue(visionTag, visionActionQueue)
    controller.addActionQueue(controllerTag, controllerActionQueue)
    controller.changeExecutionQueue(visionTag)

    client11.publish(Topics.EV3_REQUEST_NEXT)
    print("> Controller started...")
    print("> EV3 next action published. EV3's should start working")

def onSwitchExecutionThread(client, userdata, msg, controller):
    tag = msg.payload.decode()
    switched = controller.changeExecutionQueue(tag)
    if switched:
        print("> Execution thread switched to {0}".format(tag))
    else:
        print("> Execution thread not switched to {0}".format(tag))

def forwardAction(action):
    def curriedForwardedAction(client, userdata, msg, controller):
        controller.changeExecutionQueue(controllerTag)
        payload = msg.payload.decode()
        controller.actionQueues[controllerTag].put({
            "action": action,
            "payload": payload
        })
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
        return
    if currentExecThread.waiting():
        print(">>> Thread was waiting")
        currentExecThread.state.waiting = False
    if currentExecThread.locked():
        print(">>> Execution thread is locked. Actions can't be performed")
        return
    if currentExecThread.pending():
        if not currentExecThread.empty():
            client.publish(Topics.EV3_REQUEST_NEXT)
        else:
            print("> No actions left in the execution queue")
    # controller.unlockCurrentExecutionQueue()
    # print("> EV3 Action Completed")
    # currentExecutionQueue = controller.currentExecutionQueue
    # if not controller.actionQueues[currentExecutionQueue].empty():
    #     client.publish(Topics.EV3_REQUEST_NEXT)
    # else:
    #     print("> No actions left in the {0} queue".format(currentExecutionQueue))

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
    if currentExecThread.locked():
        print("> Current execution thread is locked")
        return
    if currentExecThread.waiting():
        print("> Action is not finished on EV3. Can't perform any actions!")
        return
    if currentExecThread.running():
        if not currentExecThread.empty():
            nextAction = controller.nextAction()
            # controller.lockCurrentExecutionThread()
            client11.publish(
                nextAction["action"],
                nextAction["payload"])
            client31.publish(
                nextAction["action"],
                nextAction["payload"])
            currentExecThread.state.waiting = True
            print("> Next action sent to ev3")
        else:
            print("> No actions in execution thread!")

def onEV3Stop(client, userdata, msg, controller):
    """This will stop execution on the ev3, and the current action performing
    will not finish!. It will stop in the current position. It only acts on the
    current execution thread
    """
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.lock()
    currentExecThread.state.waiting = False
    client11.publish(Topics.EV3_STOP)
    client31.publish(Topics.EV3_STOP)
    print("> Action queue locked. Ev3s are STOPPED")

def onEV3Resume(client, userdata, msg, controller):
    """This will resume the execution of the current execution thread.
    """
    client11.publish(Topics.EV3_RESUME)
    client31.publish(Topics.EV3_RESUME)
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.unlock()
    print("> Execution thread unlocked and ready to resume")
    if currentExecThread.pending():
        client11.publish(Topics.EV3_REQUEST_NEXT)

def onEV3Pause(client, userdata, msg, controller):
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.lock()
    client11.publish(Topics.EV3_PAUSE)
    client31.publish(Topics.EV3_PAUSE)
    print("> Action queue is locked and ev3s are PAUSED")
    return

def onPrintStates(client, userdata, msg, controller):
    print("> These are the current execution threads: ")
    for tag in controller.actionQueues:
        print("{0} => {1} with actions:".format(
            tag,
            controller.actionQueues[tag].state),
            controller.actionQueues[tag])

def onDeleteFirstAction(client, userdata, msg, controller):
    currentExecThread = controller.currentExecutionThread()
    if not currentExecThread.state.locked:
        print("> Current execution thread must be locked!")
        print("> First action was NOT deleted.")
        return
    else:
        # call on controller because it checks if the action is empty!
        controller.removeFirstAction()
        print("> First action WAS deleted.")

controller = Controller()
subscribedTopics = {
    # controller related
    Topics.START_CONTROLLER: onStartController,
    Topics.SWITCH_CONTROLLER_EXEC: onSwitchExecutionThread,
    Topics.CONTROLLER_DELETE_FIRST: onDeleteFirstAction,
    # the controller will only forwards to ev3
    Topics.CONTROLLER_MOVE_X: forwardAction(Topics.EV3_MOVE_X),
    Topics.CONTROLLER_MOVE_Y: forwardAction(Topics.EV3_MOVE_Y),
    Topics.CONTROLLER_MOVE_Z: forwardAction(Topics.EV3_MOVE_Z),
    Topics.CONTROLLER_GRAB: forwardAction(Topics.EV3_MOVE_GRAB),
    Topics.CONTROLLER_RELEASE: forwardAction(Topics.EV3_MOVE_RELEASE),
    Topics.CONTROLLER_RESET_X: forwardAction(Topics.EV3_RESET_X),
    Topics.CONTROLLER_RESET_Y: forwardAction(Topics.EV3_RESET_Y),
    # ev3 related
    Topics.STOP_CONTROLLER: onEV3Stop,
    Topics.PAUSE_CONTROLLER: onEV3Pause,
    Topics.RESUME_CONTROLLER: onEV3Resume,
    # client-controller related
    Topics.CONTROLLER_PRINT_STATES: onPrintStates,
}

def onConnect(client, userdata, flags, rc):
    print("Controller listening to messages")
    for key in subscribedTopics.keys():
        client.subscribe(key)

def onMessage(client, userdata, msg):
    if msg.topic in subscribedTopics.keys():
        subscribedTopics[msg.topic](client, userdata, msg, controller)
    else:
        print("Topic {0} is not subscribed".format(msg.topic))

client11.connect(config["ips"]["INF_11"], 1883, 60)
client31.connect(config["ips"]["INF_31"], 1883, 60)
controllerClient.connect(config["ips"]["CONTROLLER"], 1883, 60)

def onEV3Connect(client, userdata, flags, rc):
    client.subscribe(Topics.EV3_REQUEST_NEXT)
    client.subscribe(Topics.EV3_ACTION_COMPLETED)

def onEV3Message(client, userdata, msg):
    if msg.topic == Topics.EV3_REQUEST_NEXT:
        onRequestNextEV3Action(client, userdata, msg, controller)
    elif msg.topic == Topics.EV3_ACTION_COMPLETED:
        onEV3ActionCompleted(client, userdata, msg, controller)

client11.on_connect = onEV3Connect
client31.on_connect = onEV3Connect
client11.on_message = onEV3Message
client31.on_message = onEV3Message

controllerClient.on_connect = onConnect
controllerClient.on_message = onMessage

client11.loop_start()
client31.loop_start()
controllerClient.loop_forever()
