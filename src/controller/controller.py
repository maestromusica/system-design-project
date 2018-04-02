#! /usr/bin/env python3
import json
import paho.mqtt.client as mqtt
import time
import os
import atexit

from ._controller import Controller
from ..utils.action_queue import ActionQueue
from .controller_functions import *
from .ev3_functions import *

configPath = os.path.join(os.path.dirname(__file__), "../config/config.json")
config = json.load(open(configPath))
topicsPath = os.path.join(os.path.dirname(__file__), "../config/topics.json")
topics = json.load(open(topicsPath))

controller = Controller()
controllerClient = mqtt.Client()
ev3 = EV3Client(controllerClient)

def connectEV3(restart=False):
    # ev3 = EV3Client(controllerClient)
    if restart:
        ev3.restart()
    ev3.on_connect(onEV3Connect)
    ev3.on_message(onEV3Message)
    ev3.on_disconnect(onEV3Disconnect)
    ev3.connect()
    ev3.loop_start()

def onAppConnectEV3(client, ev3, msg, controller):
    print("> App wants to connect the ev3s")
    connectEV3(True)
    sendData("connection", client, controller, ev3)

subscribedTopics = {
    # controller related
    topics["START_CONTROLLER"]: onStartController,
    topics["PROCESS_CONTROLLER"]: onProcess,
    topics["PROCESS_RESPONSE_CONTROLLER"]: onProcessResponse,
    topics["PROCESS_CONTROLLER_ID"]: onProcessReceiveId,
    topics["SWITCH_CONTROLLER_EXEC"]: onSwitchExecutionThread,
    topics["CONTROLLER_DELETE"]: onDelete,
    topics["SWITCH_EXEC_PENDING"]: onSwitchToPending,
    topics["SWITCH_EXEC_NOT_PENDING"]: onSwitchToNotPending,
    topics["CONTROLLER_NEXT_ACTION"]: onNext,
    # the controller will forward to ev3
    topics["CONTROLLER_MOVE_X"]: forwardAction(topics["EV3_MOVE_X"]),
    topics["CONTROLLER_MOVE_Y"]: forwardAction(topics["EV3_MOVE_Y"]),
    topics["CONTROLLER_MOVE_Z"]: forwardAction(topics["EV3_MOVE_Z"]),
    topics["CONTROLLER_GRAB"]: forwardAction(topics["EV3_MOVE_GRAB"]),
    topics["CONTROLLER_RELEASE"]: forwardAction(topics["EV3_MOVE_RELEASE"]),
    topics["CONTROLLER_ROTATE"]: forwardAction(topics["EV3_ROTATE"]),
    topics["CONTROLLER_RESET_X"]: forwardAction(topics["EV3_RESET_X"]),
    topics["CONTROLLER_RESET_Y"]: forwardAction(topics["EV3_RESET_Y"]),
    topics["CONTROLLER_RESET_Z"]: forwardAction(topics["EV3_RESET_Z"]),
    # ev3 related
    topics["STOP_CONTROLLER"]: onEV3Stop,
    topics["PAUSE_CONTROLLER"]: onEV3Pause,
    topics["RESUME_CONTROLLER"]: onEV3Resume,
    # client-controller related
    topics["CONTROLLER_PRINT_STATES"]: onPrintStates,
    topics["CONTROLLER_PRINT_POS"]: onPrintPositions,

    topics["APP_REQUEST"]: onAppRequestData,
    topics["APP_REQUEST_IMG"]: onAppRequestImg,
    topics["APP_REQUEST_BOXES"]: onAppRequestBoxes,
    topics["EV3_CONNECTED"]: onEV3Connected,

    topics["APP_CONNECT_EV3"]: onAppConnectEV3,

    topics["CONTROLLER_SAVE_IP_11"]: onAppSaveEV11IP,
    topics["CONTROLLER_SAVE_IP_31"]: onAppSaveEV31IP,
    topics["CONN"]: onAppConn,

    topics["RESUME_SORTING"]: onResumeSorting,
    topics["PAUSE_SORTING"]: onPauseSorting,
    topics["END_SORTING"]: onEndSorting
}

def onConnect(client, userdata, flags, rc):
    print("Controller listening to messages")
    visionTag = "vision"
    controllerTag = "controller"

    visionActionQueue = ActionQueue(pending=False)
    controllerActionQueue = ActionQueue()

    controller.addActionQueue(visionTag, visionActionQueue)
    controller.addActionQueue(controllerTag, controllerActionQueue)
    controller.changeExecutionQueue(visionTag)

    for key in subscribedTopics.keys():
        client.subscribe(key)

    ev3.on_connect(onEV3Connect)
    ev3.on_message(onEV3Message)
    ev3.on_disconnect(onEV3Disconnect)
    ev3.connect()
    ev3.loop_start()
    onStartController(controllerClient, ev3, "", controller)
    client.publish(topics["CONN_ACK"])

def onDisconnect():
    controllerClient.publish(topics["CONN_DISABLE"])

def onMessage(client, userdata, msg):
    if msg.topic in subscribedTopics.keys():
        subscribedTopics[msg.topic](controllerClient, ev3, msg, controller)
    else:
        print("Topic {0} is not subscribed".format(msg.topic))

def onPrint(client, userdata, msg, controller):
    print(msg.payload.decode())

ev3SubscribedTopics = {
    topics["EV3_REQUEST_NEXT"]: onRequestNextEV3Action,
    topics["EV3_ACTION_COMPLETED"]: onEV3ActionCompleted,
    topics["CONTROLLER_PRINT"]: onPrint,
    topics["EV3_CONN_ACK"]: onEV3ConnectionAck
}

def onEV3Connect(client, userdata, flags, rc):
    for topic in ev3SubscribedTopics.keys():
        client.subscribe(topic)
    ev3.publish(topics["EV3_CONN"])
    sendData("connection", controllerClient, controller, ev3)

def onEV3Message(client, userdata, msg):
    if msg.topic in ev3SubscribedTopics.keys():
        ev3SubscribedTopics[msg.topic](controllerClient, ev3, msg, controller)
    else:
        print("Topic {0} is not subscribed".format(msg.topic))

def onEV3Disconnect(client, userdata, rc):
    print(">>> EV3 disconneted")
    ev3.setDisconnected("all")
    sendData("connection", controllerClient, controller, ev3)

controllerClient.on_connect = onConnect
controllerClient.on_message = onMessage
controllerClient.on_disconnect = onDisconnect
atexit.register(onDisconnect)
controllerClient.connect(config["ips"]["CONTROLLER"], 1883, 60)
controllerClient.loop_forever()
