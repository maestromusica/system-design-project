#! /usr/bin/env python3
import json
import paho.mqtt.client as mqtt
import time
import os

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

subscribedTopics = {
    # controller related
    topics["START_CONTROLLER"]: onStartController,
    topics["PROCESS_CONTROLLER"]: onProcess,
    topics["PROCESS_RESPONSE_CONTROLLER"]: onProcessResponse,
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
    topics["EV3_CONNECTED"]: onEV3Connected,

    topics["CONTROLLER_SAVE_IP_11"]: onAppSaveEV11IP,
    topics["CONTROLLER_SAVE_IP_31"]: onAppSaveEV31IP
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
    client.publish(topics["APP_REQUEST"], "all")

    ev3.on_connect(onEV3Connect)
    ev3.on_message(onEV3Message)
    ev3.connect({
        "ip": config["ips"]["INF_11"],
        "port": 1883,
        "keepalive": 60
    }, {
        "ip": config["ips"]["INF_31"],
        "port": 1883,
        "keepalive": 60
    })
    ev3.loop_start()

def onMessage(client, userdata, msg):
    if msg.topic in subscribedTopics.keys():
        subscribedTopics[msg.topic](controllerClient, ev3, msg, controller)
        if not msg.topic == topics["APP_REQUEST"]:
            client.publish(topics["APP_REQUEST"], "all")
    else:
        print("Topic {0} is not subscribed".format(msg.topic))

def onPrint(client, userdata, msg, controller):
    print(msg.payload.decode())

def onEV3Connect(client, userdata, flags, rc):
    ev3.subscribe(topics["EV3_REQUEST_NEXT"])
    ev3.subscribe(topics["EV3_ACTION_COMPLETED"])
    ev3.subscribe(topics["CONTROLLER_PRINT"])
    ev3.deviceConnected()

def onEV3Message(client, userdata, msg):
    if msg.topic == topics["EV3_REQUEST_NEXT"]:
        onRequestNextEV3Action(client, ev3, msg, controller)
    elif msg.topic == topics["EV3_ACTION_COMPLETED"]:
        onEV3ActionCompleted(client, ev3, msg, controller)
    elif msg.topic == topics["CONTROLLER_PRINT"]:
        onPrint(client, userdata, msg, controller)

controllerClient.on_connect = onConnect
controllerClient.on_message = onMessage
controllerClient.connect(config["ips"]["CONTROLLER"], 1883, 60)
controllerClient.loop_forever()
