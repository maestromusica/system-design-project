#! /usr/bin/env python3
from cmd import Cmd
import paho.mqtt.client as mqtt
import time
import json
from message_types import Topics


class ControllerPrompt(Cmd):
    def __init__(self, client):
        super(ControllerPrompt, self).__init__()

        self.client = client
        self.client.connect("127.0.0.1", 1883, 60)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flag, rc):
        self.client.subscribe(Topics.RECIEVE_DATA_BOXES)
        self.client.subscribe(Topics.RECIEVE_DATA_NEXT)

    def _on_message(self, client, userdata, msg):
        if msg.topic == Topics.RECIEVE_DATA_BOXES:
            print(msg.payload.decode())
        elif msg.topic == Topics.RECIEVE_DATA_NEXT:
            print(msg.payload.decode())

    def do_start(self, args):
        """Starts the system and polls for an image"""
        if len(args) > 0:
            print("Start doesn't allow arguments!")
        else:
            print("Starting the controller...")
            self.client.publish(Topics.START_CONTROLLER)

    def do_stop(self, args):
        print("Stopping the controller")
        self.client.publish(Topics.STOP_CONTROLLER)

    def do_print(self, args):
        if len(args) == 0:
            print("What do you want to print?")
        elif args == "boxes":
            self.client.publish(Topics.REQUEST_DATA_BOXES)
            time.sleep(1)
        elif args == "next":
            self.client.publish(Topics.REQUEST_DATA_NEXT)
            time.sleep(1)
        else:
            print(args)

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting")
        self.client.loop_stop()
        self.client.disconnect()
        raise SystemExit

if __name__ == "__main__":
    client = mqtt.Client()

    prompt = ControllerPrompt(client)

    prompt.client.loop_start()

    prompt.prompt = "> "
    prompt.cmdloop("Starting controller prompt ... ")
