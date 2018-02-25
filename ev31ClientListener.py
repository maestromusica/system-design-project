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
    client.publish(Topics.EV3_ACTION_COMPLETED)

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

def onPause(client, userdata, msg):
    pass

subscribedTopics = {
    Topics.EV3_MOVE_X: onMoveX,
    Topics.EV3_STOP: onStop,
    Topics.EV3_RESUME: onResume,
    Topics.EV3_PAUSE: onPause,
    Topics.EV3_RESET_X: onResetX
}

def onConnect(client, userdata, flags, rc):
    print("EV_31 Client connected!")
    print("======== SortX ========")
    for topic in subscribedTopics.keys():
        client.subscribe(topic)

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
            client.publish(Topics.EV3_ACTION_COMPLETED)
        flag = 0
    time.sleep(.01)
