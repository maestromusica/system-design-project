#! /usr/bin/env python3
import paho.mqtt.client as mqtt
from message_types import Topics
import time

state = "RUNNING"

def onEV3Action(client, userdata, msg):
    print("> Topic is: ", msg.topic)
    print("> Payload is: ", msg.payload.decode())
    print("> Action completed")
    time.sleep(1)
    client.publish(Topics.EV3_ACTION_COMPLETED)

def onEV3Stop(client, userdata, msg):
    print("> EV3 stop not implemented")

def onEV3Resume(client, userdata, msg):
    print("> EV3 resume not implemented")

def onEV3Pause(client, userdata, msg):
    print("> EV3 Pause not implemented")

def onPrint(client, userdata, msg):
    print("xax1: 900")
    client.publish(Topics.CONTROLLER_PRINT, "xax1: 900")

subscribedTopics = {
    Topics.EV3_MOVE_X: onEV3Action,
    Topics.EV3_MOVE_Y: onEV3Action,
    Topics.EV3_MOVE_Z: onEV3Action,
    Topics.EV3_MOVE_GRAB: onEV3Action,
    Topics.EV3_MOVE_RELEASE: onEV3Action,
    Topics.EV3_RESET_X: onEV3Action,
    Topics.EV3_RESET_Y: onEV3Action,
    Topics.EV3_RESET_Z: onEV3Action,
    Topics.EV3_STOP: onEV3Stop,
    Topics.EV3_RESUME: onEV3Resume,
    Topics.EV3_PAUSE: onEV3Pause,
    Topics.EV3_PRINT_POS: onPrint
}

def onConnect(client, userdata, flags, rc):
    print("> Connected")
    for topic in subscribedTopics.keys():
        client.subscribe(topic)

def onMessage(client, userdata, msg):
    if msg.topic in subscribedTopics.keys():
        subscribedTopics[msg.topic](client, userdata, msg)
    else:
        print("Topic not found")

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
client.on_message = onMessage
client.on_connect = onConnect
client.loop_forever()
