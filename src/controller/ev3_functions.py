import json
import paho.mqtt.client as mqtt
import os

topicsPath = os.path.join(os.path.dirname(__file__), "../config/topics.json")
topics = json.load(open(topicsPath))

visionTag = "vision"
controllerTag = "controller"

def onEV3ActionCompleted(client, ev3, msg, controller):
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
        client.publish(topics["APP_REQUEST"], "all")
        return
    if currentExecThread.waiting():
        print(">>> Thread was waiting")
        currentExecThread.state.waiting = False
    if currentExecThread.locked():
        print(">>> Execution thread is locked. Actions can't be performed")
        client.publish(topics["APP_REQUEST"], "all")
        return
    if currentExecThread.pending():
        if not currentExecThread.empty():
            client.publish(topics["EV3_REQUEST_NEXT"])
        else:
            print("> No actions left in the execution queue")
    client.publish(topics["APP_REQUEST"], "all")

def onRequestNextEV3Action(client, ev3, msg, controller):
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
    client.publish(topics["APP_REQUEST"], "all")
    if currentExecThread.locked():
        print("> Current execution thread is locked")
        return
    if currentExecThread.waiting():
        print("> Action is not finished on EV3. Can't perform any actions!")
        return
    if currentExecThread.running():
        if not currentExecThread.empty():
            nextAction = controller.nextAction()
            ev3.publish(nextAction["action"], nextAction["payload"])
            currentExecThread.state.waiting = True
            print("> Next action sent to ev3")
        else:
            print("> No actions in execution thread!")
    client.publish(topics["APP_REQUEST"], "all")

def onEV3Stop(client, ev3, msg, controller):
    """This will stop execution on the ev3, and the current action performing
    will not finish!. It will stop in the current position. It only acts on the
    current execution thread
    """
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.lock()
    currentExecThread.state.waiting = False
    ev3.publish(topics["EV3_STOP"])
    print("> Action queue locked. Ev3s are STOPPED")

def onEV3Resume(client, ev3, msg, controller):
    """This will resume the execution of the current execution thread.
    """
    ev3.publish(topics["EV3_RESUME"])
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.unlock()
    print("> Execution thread unlocked and ready to resume")
    if currentExecThread.pending():
        ev3.publish(topics["EV3_REQUEST_NEXT"])

def onEV3Pause(client, ev3, msg, controller):
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.lock()
    ev3.publish(topics["EV3_PAUSE"])
    print("> Action queue is locked and ev3s are PAUSED")
    return

class EV3Client():
    def __init__(self, controllerClient):
        self.client11 = mqtt.Client()
        self.client31 = mqtt.Client()
        self.controllerClient = controllerClient
        self.devicesConnected = 0

    def connect(self, ev11, ev31):
        self.client11.connect(ev11["ip"], ev11["port"], ev11["keepalive"])
        # self.client31.connect(ev31["ip"], ev31["port"], ev31["keepalive"])

    def publish(self, topic, message=None):
        if(topic == topics["EV3_REQUEST_NEXT"]):
            self.client11.publish(topic, message)
        else:
            self.client11.publish(topic, message)
            # self.client31.publish(topic, message)

    def subscribe(self, topic):
        self.client11.subscribe(topic)
        # self.client31.subscribe(topic)

    def loop_start(self):
        self.client11.loop_start()
        # self.client31.loop_start()

    def on_connect(self, function):
        self.client11.on_connect = function
        # self.client31.on_connect = function

    def on_message(self, function):
        self.client11.on_message = function
        # self.client31.on_message = function

    def deviceConnected(self):
        self.devicesConnected += 1
        if self.devicesConnected == 1:
            self.controllerClient.publish(topics["EV3_CONNECTED"])
