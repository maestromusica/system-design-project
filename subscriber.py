#! /usr/bin/env python3
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("topic/test")

def on_message(client, userdata, msg):
    if msg.payload.decode() == "Hello World!":
        print("Yes!")

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
