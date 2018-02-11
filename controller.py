#! /usr/bin/env python3
import json
import paho.mqtt.client as mqtt
from controller_class import Controller
from message_types import Topics

controller = Controller()

def onConnect(client, userdata, flags, rc):
    print("Controller listening to messages")
    client.subscribe(Topics.REQUEST_DATA_BOXES)
    client.subscribe(Topics.START_CONTROLLER)
    client.subscribe(Topics.STOP_CONTROLLER)

def onMessage(client, userdata, msg):
    if msg.topic == Topics.START_CONTROLLER:
        controller.start()
        print("topic name: ", Topics.START_CONTROLLER)
        print("Controller started...")
    elif msg.topic == Topics.REQUEST_DATA_BOXES:
        boxes = json.dumps(controller.getBoxCoordinates())
        client.publish(Topics.RECIEVE_DATA_BOXES, boxes)
        print("topic name: ", Topics.REQUEST_DATA_BOXES)
        print("box coordinates calculated")
    elif msg.topic == Topics.STOP_CONTROLLER:
        controller.stop()
        print("topic name: ", Topics.STOP_CONTROLLER)
        print("controller stopped")

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
client.on_connect = onConnect
client.on_message = onMessage

client.loop_forever()
