#! /usr/bin/env python3
import json
import paho.mqtt.client as mqtt
from controller_class import Controller
from message_types import Topics
from action_queue import ActionQueueLockedException

controllerClient = mqtt.Client()
client11 = mqtt.Client()
client31 = mqtt.Client()

def onStartController(client, userdata, msg, controller):
    controller.start()
    client11.publish(Topics.EV3_REQUEST_NEXT)
    print("> Controller started...")
    print("> EV3 next action published. EV3's should start working")

def onStopController(client, userdata, msg, controller):
    print("> Not implemented")

def forwardAction(action):
    def curriedForwardedAction(client, userdata, msg, controller):
        print("Action sent to ev3: ", action)
        print("Payload: ", msg.payload.decode())
        payload = msg.payload.decode()
        client11.publish(action, payload)
        client31.publish(action, payload)

    return curriedForwardedAction

def onRequestNextEV3Action(client, userdata, msg, controller):
    # this is recieved from the ev3 machine and it will output the next action
    try:
        nextAction = controller.nextAction()
        if nextAction is None:
            print("> No actions left")
            return

        client11.publish(nextAction["action"], json.dumps(nextAction["payload"]))
        client31.publish(nextAction["action"], json.dumps(nextAction["payload"]))
        print("> Next action sent")
    except ActionQueueLockedException:
        print("> Can't send next action cuz the queue is locked!")
        controller.pendingAction = True


def onEV3Stop(client, userdata, msg, controller):
    controller.lockQueue()
    print("> Action queue locked. This should stop ev3 execution")

def onEV3Resume(client, userdata, msg, controller):
    if controller.pendingAction:
        client11.publish(Topics.EV3_REQUEST_NEXT)
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
    # the controller will only forwards to ev3
    Topics.CONTROLLER_MOVE_X: forwardAction(Topics.EV3_MOVE_X),
    Topics.CONTROLLER_MOVE_Y: forwardAction(Topics.EV3_MOVE_Y),
    Topics.CONTROLLER_MOVE_Z: forwardAction(Topics.EV3_MOVE_Z),
    # ev3 related
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

# TODO: replace with file readings
client11.connect("169.254.201.116", 1883, 60)
client31.connect("169.254.251.241", 1883, 60)
controllerClient.connect("127.0.0.1", 1883, 60)

def onEV3Connect(client, userdata, flags, rc):
    client.subscribe(Topics.EV3_REQUEST_NEXT)

def onEV3Message(client, userdata, msg):
    onRequestNextEV3Action(client, userdata, msg, controller)

client11.on_connect = onEV3Connect
client31.on_connect = onEV3Connect
client11.on_message = onEV3Message
client31.on_message = onEV3Message

controllerClient.on_connect = onConnect
controllerClient.on_message = onMessage

client11.loop_start()
client31.loop_start()
controllerClient.loop_forever()
