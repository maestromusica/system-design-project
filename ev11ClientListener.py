#! /usr/bin/env python3
import paho.mqtt.client as mqtt
from message_types import Topics
import time

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)

def onMoveX(client, userdata, msg):
    client.publish(Topics.EV3_REQUEST_NEXT)
    time.sleep(1)
    pass

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
    Topics.EV3_FORCE_STOP: onForceStop
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
