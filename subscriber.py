#! /usr/bin/env python3
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("topic/test")
    client.subscribe("topic/send")

def on_message(client, userdata, msg):
    if msg.topic == "topic/send":
        client.publish("topic/recieve", json.dumps([
            {
                "length": 100,
                "width": 200,
                "height": 40
            },
            {
                "length": 40,
                "width": 20,
                "height": 90
            },
            {
                "length": 10,
                "width": 40,
                "height": 500
            }
            ]
        ))
    if msg.payload.decode() == "Hello World!":
        print("Yes!")

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
