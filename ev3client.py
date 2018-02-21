#! /usr/bin/env python3
import paho.mqtt.client as mqtt
from message_types import Topics
import time

def onEV3Action(client, userdata, msg):
    print("> Topic is: ", msg.topic)
    print("> Payload is: ", msg.payload.decode())
    time.sleep(1)
    print("> Action completed")
    client.publish(Topics.EV3_ACTION_COMPLETED)

def onEV3Stop(client, userdata, msg):
    print("> EV3 stop not implemented")

def onEV3Resume(client, userdata, msg):
    print("> EV3 resume not implemented")

def onEV3ForceStop(client, userdata, msg):
    print("> it should stop all the motors at all cost")
    # Important Note: if doing waitFor(motor) when running the motors
    # and we want to implement this function, then we have to take care
    # in the waitFor function for this message!
    print("> Stopping and exiting the program")
    client.loop_stop()
    raise SystemExit

subscribedTopics = {
    Topics.EV3_MOVE_X: onEV3Action,
    Topics.EV3_MOVE_Y: onEV3Action,
    Topics.EV3_MOVE_Z: onEV3Action,
    Topics.EV3_MOVE_GRAB: onEV3Action,
    Topics.EV3_MOVE_RELEASE: onEV3Action,
    Topics.EV3_RESET_X: onEV3Action,
    Topics.EV3_RESET_Y: onEV3Action,
    Topics.EV3_STOP: onEV3Stop,
    Topics.EV3_RESUME: onEV3Resume,
    Topics.EV3_FORCE_STOP: onEV3ForceStop,
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
