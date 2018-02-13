#! /usr/bin/env python3
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
client.publish("topic/test", "Hello World!")
client.disconnect()
