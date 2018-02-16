#! /usr/bin/env python
import paho.mqtt.client as mqtt
from message_types import Topics
import time

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)

def onMoveY(client, userdata, msg):
    client.publish(Topics.EV3_REQUEST_NEXT)
    time.sleep(1)

def onMoveZ(client, userdata, msg):
    client.publish(Topics.EV3_REQUEST_NEXT)
    time.sleep(1)

def onGrab(client, userdata, msg):
    client.publish(Topics.EV3_REQUEST_NEXT)
    time.sleep(1)

def onRelease(client, userdata, msg):
    client.publish(Topics.EV3_REQUEST_NEXT)
    time.sleep(1)

def onStop(client, userdata, msg):
    pass

def onResume(client, userdata, msg):
    pass

def onForceStop(client, userdata, msg):
    pass

subscribedTopics = {
    Topics.EV3_MOVE_Y: onMoveY,
    Topics.EV3_MOVE_Z: onMoveZ,
    Topics.EV3_MOVE_GRAB: onGrab,
    Topics.EV3_MOVE_RELEASE: onRelease,
    Topics.EV3_STOP: onStop,
    Topics.EV3_RESUME: onResume,
    Topics.EV3_FORCE_STOP: onForceStop
}

def onConnect(client, userdata, flags, rc):
    print("EV3_31 Client connected!")
    print("======== SortX ========")
    for topic in subscribedTopics.keys():
        client.subscribe(topic)

def onMessage(client, userdata, msg):
    subscribedTopics[msg.topic](client, userdata, msg)
    print("Action Executed: ", msg.topic)
    print("Payload: ", msg.payload.decode())

client.on_connect = onConnect
client.on_message = onMessage
client.loop_forever()
