#! /usr/bin/env python3
import paho.mqtt.client as mqtt
from message_types import Topics
from motors11 import *
from utils.motors import waitFor, waitForStalled
import time

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)

flag = 0
stop = False

def onResetY(client, userdata, msg):
    resetYAxis() # reset axis doesn't need stop function
    client.publish(Topics.EV3_ACTION_COMPLETED)

def onMoveY(client, userdata, msg):
    global flag

    position = int(msg.payload.decode())
    speed = 300

    moveY(position, speed)
    flag = 1

def onMoveZ(client, userdata, msg):
    global flag
    position = int(msg.payload.decode())
    speed = 200

    moveZ(position, speed)
    flag = 2

def onGrab(client, userdata, msg):
    global flag
    position = int(msg.payload.decode())
    speed = 100

    moveGrabber(position, speed)
    flag = 3

def onRelease(client, userdata, msg):
    global flag
    position = int(msg.payload.decode())
    speed = 100

    moveGrabber(position, speed)
    flag = 3

def onStop(client, userdata, msg):
    global stop

    stop = True
    # TODO: refactor here to stop only the moving motors
    yax1.stop()
    yax2.stop()
    zax.stop()
    grabber.stop()

def onResume(client, userdata, msg):
    global stop
    stop = False

def onPause(client, userdata, msg):
    pass

def onPrint(client, userdata, msg):
    client.publish(Topics.CONTROLLER_PRINT, "yax1: {0}".format(yax1.position_sp))
    client.publish(Topics.CONTROLLER_PRINT, "yax2: {0}".format(yax2.position_sp))
    client.publish(Topics.CONTROLLER_PRINT, "zax: {0}".format(zax.position_sp))
    client.publish(Topics.CONTROLLER_PRINT, "grabber: {0}".format(grabber.position_sp))

subscribedTopics = {
    Topics.EV3_MOVE_Y: onMoveY,
    Topics.EV3_MOVE_Z: onMoveZ,
    Topics.EV3_MOVE_GRAB: onGrab,
    Topics.EV3_MOVE_RELEASE: onRelease,
    Topics.EV3_STOP: onStop,
    Topics.EV3_RESUME: onResume,
    Topics.EV3_PAUSE: onPause,
    Topics.EV3_RESET_Y: onResetY,
    Topics.EV3_PRINT_POS: onPrint
}

def onConnect(client, userdata, flags, rc):
    print("EV3_11 Client connected!")
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
        while "running" in yax1.state and not stop:
            time.sleep(.01)
        if stop:
            stop = False
        else:
            client.publish(Topics.EV3_ACTION_COMPLETED)
        flag = 0
    elif flag == 2:
        while "running" in zax.state and not stop:
            time.sleep(.01)
        if stop:
            stop = False
        else:
            client.publish(Topics.EV3_ACTION_COMPLETED)
        flag = 0
    elif flag == 3:
        while "running" in grabber.state and "stalled" not in grabber.state and not stop:
            time.sleep(.01)
        if stop:
            stop = False
        else:
            client.publish(Topics.EV3_ACTION_COMPLETED)
        flag = 0
    time.sleep(.01)
