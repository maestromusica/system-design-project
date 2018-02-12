#! /usr/bin/env python3
import json
import paho.mqtt.client as mqtt
from controller_class import Controller
from message_types import Topics
from action_queue import ActionQueueLockedException

def onStartController(client, userdata, msg, controller):
    controller.start()
    client.publish(Topics.EV3_REQUEST_NEXT)
    print("> Controller started...")
    print("> EV3 next action published. EV3's should start working")

def onStopController(client, userdata, msg, controller):
    print("> Not implemented")

def onRequestNextEV3Action(client, userdata, msg, controller):
    # this is recieved from the ev3 machine and it will output the next action
    try:
        nextAction = controller.nextAction()
        if nextAction is None:
            print("> No actions left")
            return

        client.publish(nextAction["action"], json.dumps(nextAction["payload"]))
        print("> Next action sent")
    except ActionQueueLockedException:
        controller.pendingAction = True


def onEV3Stop(client, userdata, msg, controller):
    controller.lockQueue()
    print("> Action queue locked. This should stop ev3 execution")

def onEV3Resume(client, userdata, msg, controller):
    if controller.pendingAction:
        client.publish(Topics.EV3_REQUEST_NEXT)
    controller.unlockQueue()
    print("> Action queue is now unlocked")

def onEV3ForceStop(client, userdata, msg, controller):
    # TODO: define the behaviour of the controller in this case
    # print("> Force stopping the EV3")
    return

def onRequestDataBoxes(client, userdata, msg, controller):
    boxes = json.dumps(controller.getBoxCoordinates())
    client.publish(Topics.RECIEVE_DATA_BOXES, boxes)
    print("topic name: ", Topics.REQUEST_DATA_BOXES)
    print("box coordinates calculated")

controller = Controller()
subscribedTopics = {
    # controller related
    Topics.START_CONTROLLER: onStartController,
    Topics.STOP_CONTROLLER: onStopController,
    # ev3 related
    Topics.EV3_REQUEST_NEXT: onRequestNextEV3Action,
    Topics.EV3_STOP: onEV3Stop,
    Topics.EV3_RESUME: onEV3Resume,
    Topics.EV3_FORCE_STOP: onEV3ForceStop,
    # client related
    Topics.REQUEST_DATA_BOXES: onRequestDataBoxes,
}

def onConnect(client, userdata, flags, rc):
    print("Controller listening to messages")
    for key in subscribedTopics.keys():
        client.subscribe(key)

def onMessage(client, userdata, msg):
    if msg.topic in subscribedTopics.keys():
        subscribedTopics[msg.topic](client, userdata, msg, controller)
    else:
        print("Topic {0} is not subscribed".format(msg.topic))

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
client.on_connect = onConnect
client.on_message = onMessage

client.loop_forever()
