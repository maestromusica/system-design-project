#! /usr/bin/env python3
import paho.mqtt.client as mqtt
from message_types import Topics
from motors31 import *
from utils.motors import waitFor
import time

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)

"""
flag states:
- 0: initial state, doesn't happen anything
- 1: motors 1 and 2 are running
- 2: ?!
"""
flag = 0
stop = False

def onResetX(client, uesrdata, msg):
    resetXAxis()
    client.publish(topics["EV3_ACTION_COMPLETED"])

def onMoveX(client, userdata, msg):
    global flag

    position = int(msg.payload.decode())
    speed = 300

    moveX(position, speed)
    flag = 1

def onStop(client, userdata, msg):
    global stop

    stop = True
    xax1.stop()
    xax2.stop()

def onResume(client, userdata, msg):
    global stop

    stop = False

def onRotate(client,userdata, msg):
    rotate(msg.payload.decode(),300)

def onGrab(client, userdata, msg):
    grab(msg.payload.decode(),300)

def onRelease(client, userdata, msg):
    grab(msg.payload.decode(),300)

def onPause(client, userdata, msg):
    pass

def onPrint(client, userdata, msg):
    client.publish(topics["CONTROLLER_PRINT"], "xax1: {0}".format(xax1.position_sp))
    client.publish(topics["CONTROLLER_PRINT"], "xax2: {0}".format(xax2.position_sp))

subscribedTopics = {
    topics["EV3_MOVE_X"]: onMoveX,
    topics["EV3_STOP"]: onStop,
    topics["EV3_RESUME"]: onResume,
    topics["EV3_PAUSE"]: onPause,
    topics["EV3_RESET_X"]: onResetX,
    topics["EV3_PRINT_POS"]: onPrint,
    topics["EV3_ROTATE"] : onRotate,
    topics["EV3_MOVE_GRAB"] : onGrab,
    topics["EV3_MOVE_RELEASE"] : onRelease
}

def onConnect(client, userdata, flags, rc):
    for topic in subscribedTopics.keys():
        client.subscribe(topic)
    print("EV_31 Client connected!")
    print("======== SortX ========")

def onMessage(client, userdata, msg):
    print("Action Executed: ", msg.topic)
    print("Payload: ", msg.payload.decode())
    subscribedTopics[msg.topic](client, userdata, msg)

client.on_connect = onConnect
client.on_message = onMessage
client.loop_start()

while True:
    if flag == 1:
        while "running" in xax1.state and not stop:
            time.sleep(.01)
        if stop:
            stop = False
        else:
            client.publish(topics["EV3_ACTION_COMPLETED"])
        flag = 0
    time.sleep(.01)
