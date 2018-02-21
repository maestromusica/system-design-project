#! /usr/bin/env python3
from cmd import Cmd
import paho.mqtt.client as mqtt
import time
import json
from message_types import Topics


class ClientPrompt(Cmd):
    def __init__(self, client):
        super(ClientPrompt, self).__init__()

        self.client = client
        self.client.connect("127.0.0.1", 1883, 60)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flag, rc):
        pass

    def _on_message(self, client, userdata, msg):
        pass

    def do_moveX(self, args):
        if args == "start":
            print("Not implemented")
            return
        else:
            try:
                absPos = int(args)
                self.client.publish(Topics.CONTROLLER_MOVE_X, absPos)
            except TypeError:
                print("Can move to either a float or \"start\"")

    def do_moveY(self, args):
        if args == "start":
            print("Not implemented")
            return
        else:
            try:
                absPos = int(args)
                self.client.publish(Topics.CONTROLLER_MOVE_Y, absPos)
            except TypeError:
                print("Can move to either a float or to \"start\"")

    def do_resetX(self, args):
        self.client.publish(Topics.CONTROLLER_RESET_X)

    def do_moveZ(self, args):
        if args == "start":
            print("Not implemented")
            return
        else:
            try:
                absPos = int(args)
                self.client.publish(Topics.CONTROLLER_MOVE_Z, absPos)
            except TypeError:
                print("Can move to either a float or to \"start\"")

    def do_resetY(self, args):
        self.client.publish(Topics.CONTROLLER_RESET_Y)

    def do_start(self, args):
        """Starts the system and polls for an image"""
        if len(args) > 0:
            print("Start doesn't allow arguments!")
        else:
            print("Starting the controller...")
            self.client.publish(Topics.START_CONTROLLER)

    def do_stop(self, args):
        if len(args) == 0:
            print("Stopping the execution thread (and the robot)")
            self.client.publish(Topics.STOP_CONTROLLER)

    def do_pause(self, args):
        if len(args) == 0:
            print("Stopping the execution thread (and the robot)")
            self.client.publish(Topics.PAUSE_CONTROLLER)

    def do_resume(self, args):
        if len(args) == 0:
            print("Resuming execution thread (and the robot)")
            self.client.publish(Topics.RESUME_CONTROLLER)

    def do_switch(self, args):
        if len(args) == 0:
            print("Must supply an execution thread tag")
            return
        else:
            print("Switching to execution thread: {0}".format(args))
            self.client.publish(Topics.SWITCH_CONTROLLER_EXEC, args)

    def do_print(self, args):
        if args == "states":
            print("Printing the states of the execution threads")
            self.client.publish(Topics.CONTROLLER_PRINT_STATES)

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting")
        self.client.loop_stop()
        self.client.disconnect()
        raise SystemExit

if __name__ == "__main__":
    client = mqtt.Client()

    prompt = ClientPrompt(client)

    prompt.client.loop_start()

    prompt.prompt = "> "
    prompt.cmdloop("Starting controller prompt ... ")
