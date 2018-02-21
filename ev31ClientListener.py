#! /usr/bin/env python
import paho.mqtt.client as mqtt
from message_types import Topics
from INF_31 import motors31
import time

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)

def onResetX(client, uesrdata, msg):
    motors31.resetXAxis()
    client.publish(Topics.EV3_REQUEST_NEXT)
    time.sleep(1)

def onMoveX(client, userdata, msg):
    position = msg.payload.decode()
    speed = 300
    motors31.moveX(position, speed)
    client.publish(Topics.EV3_REQUEST_NEXT)
    time.sleep(1)

def onStop(client, userdata, msg):
    pass

def onResume(client, userdata, msg):
    pass

def onForceStop(client, userdata, msg):
    pass

subscribedTopics = {
    Topics.EV3_MOVE_X: onMoveX,
    Topics.EV3_STOP: onStop,
    Topics.EV3_RESUME: onResume,
    Topics.EV3_FORCE_STOP: onForceStop,
    Topics.EV3_RESET_X: onResetX
}

def onConnect(client, userdata, flags, rc):
    print("EV_11 Client connected!")
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
