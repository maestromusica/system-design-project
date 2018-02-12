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
        if len(args) == 0:
            print("Stopping the controller")
            self.client.publish(Topics.STOP_CONTROLLER)
        elif args == "robot" or args == "ev3":
            print("Stopping the EV3 robots. They can be resumed")
            self.client.publish(Topics.EV3_STOP)

    def do_brake(self, args):
        if len(args) == 0:
            print("Force stopping the program")
        elif args == "robot" or args == "ev3":
            print("Braking the EV3 programs.")
            self.client.publish(Topics.EV3_FORCE_STOP)

    def do_resume(self, args):
        if len(args) == 0:
            print("Resume what?")
        elif args == "robot" or args == "ev3":
            print("Resuming program execution on the robot")
            self.client.publish(Topics.EV3_RESUME)

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
