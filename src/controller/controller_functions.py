import json
import cv2
import base64
import numpy
import os
from ..vision.System import VisionAdaptor
from ..vision.Algorithm import StackingAlgorithm
from ..config.index import boxes
from random import randrange

visionTag = "vision"
controllerTag = "controller"

topicsPath = os.path.join(os.path.dirname(__file__), "../config/topics.json")
topics = json.load(open(topicsPath))

configPath = os.path.join(os.path.dirname(__file__), "../config/config.json")

global va
va = None

def onStartController(client, ev3, msg, controller):
    global va
    va = VisionAdaptor(controller.actionQueues[visionTag])
    print("> Controller started...")

def onProcess(client, ev3, msg, controller):
    print("> On process called")
    controller.changeExecutionQueue(visionTag)
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.lock()
    client.publish(topics["CONTROLLER_DELETE"], "all")
    client.publish(topics["APP_REQUEST_IMG"])

def onProcessResponse(client, ev3, msg, controller):
    print("Hello world")
    if msg.payload.decode() == "True":
        #visionActionQueue = controller.actionQueues[visionTag]
        #quantitative1(visionActionQueue)

        # Populate the queue.
        global va
        bins = va.execute()
        sortedBoxes = adaptPackingBoxes(bins)
        client.publish(
            topics["APP_RECEIVE_VISION_BOXES"],
            json.dumps(sortedBoxes)
        )
        print(controller.actionQueues[visionTag])
        print("> Accepted")
    elif msg.payload.decode() == "False":
        print("> Not accepted")

def onSwitchExecutionThread(client, ev3, msg, controller):
    tag = msg.payload.decode()
    switched = controller.changeExecutionQueue(tag)
    if switched:
        print("> Execution thread switched to {0}".format(tag))
    else:
        print("> Execution thread not switched to {0}".format(tag))

def onSwitchToPending(client, ev3, msg, controller):
    tag = msg.payload.decode()
    execThread = None
    if tag == "":
        execThread = controller.currentExecutionThread()
    else:
        execThread = controller.actionQueues[tag]

    if execThread.state.waiting:
        print("Execution thread is waiting for an action to finish.")
        print("Please stop the execution thread and then switch to pending!")
        return

    execThread.state.pending = True
    print("Execution thread was switched to pending")

def onSwitchToNotPending(client, ev3, msg, controller):
    tag = msg.payload.decode()
    execThread = None
    if tag == "":
        execThread = controller.currentExecutionThread()
    else:
        execThread = controller.actionQueues[tag]

    if execThread.state.waiting:
        print("Execution thread is waiting for an action to finish.")
        print("Please stop the execution thread and then switch to not pending!")
        return

    execThread.state.pending = False
    print("Execution thread was switched to pending")

def forwardAction(action):
    def curriedForwardedAction(client, ev3, msg, controller):
        controller.changeExecutionQueue(controllerTag)
        client.publish(topics["APP_RECEIVE_THREAD"], controller.currentExecThreadTag)
        payload = msg.payload.decode()
        controller.actionQueues[controllerTag].put({
            "action": action,
            "payload": payload
        })
        currentExecThread = controller.currentExecutionThread()
        if currentExecThread.state.pending:
            ev3.publish(topics["EV3_REQUEST_NEXT"])
        print("> Next action added to the queue")

    return curriedForwardedAction

def onDelete(client, ev3, msg, controller):
    currentExecThread = controller.currentExecutionThread()
    payload = msg.payload.decode()
    pos = None

    if not currentExecThread.state.locked:
        print("> Current execution thread must be locked!")
        print("> Action was NOT deleted.")
        return

    if payload == "first":
        pos = 0
    elif payload == "last":
        pos = len(currentExecThread) - 1
    elif payload == "all":
        for i in range(len(currentExecThread)):
            currentExecThread.remove(0)
        print("> Deleted all actions in the queue")
        return
    else:
        # asusmed it's an integer
        pos = int(payload)

    if pos >= 0 and pos < len(currentExecThread):
        removed = currentExecThread.remove(pos)
        if removed == None:
            print("> Action was not deleted!")
        else:
            print("> Action WAS deleted.")
    else:
        print("Positional argument is not within queue boundary")
        return

def onNext(client, ev3, msg, controller):
    currentExecThread = controller.currentExecutionThread()
    if currentExecThread.state.pending:
        print("> Current exec thread is already pending")
        print("> Next action is not implemented for pending threads")
        return
    if currentExecThread.state.waiting:
        print("> Can't send next action because thread is waiting!")
        return
    if currentExecThread.state.locked:
        print("> Current exec thread is locked!")
        return
    ev3.publish(topics["EV3_REQUEST_NEXT"])
    print("> Next action should be sent to ev3.")

def onAppRequestData(client, ev3, msg, controller):
    whatToSend = msg.payload.decode()
    currentExecThread = controller.currentExecutionThread()
    if whatToSend == "thread":
        client.publish(topics["APP_RECEIVE_THREAD"], controller.currentExecThreadTag)
    elif whatToSend == "locked":
        client.publish(topics["APP_RECEIVE_LOCKED"], currentExecThread.state.locked)
    elif whatToSend == "pending":
        client.publish(topics["APP_RECEIVE_PENDING"], currentExecThread.state.pending)
    elif whatToSend == "waiting":
        client.publish(topics["APP_RECEIVE_WAITING"], currentExecThread.state.waiting)
    elif whatToSend == "actions":
        actions = numpy.array(currentExecThread.queue).tolist()
        client.publish(topics["APP_RECEIVE_ACTIONS"], json.dumps(actions))
    elif whatToSend == "connection":
        client.publish(topics["APP_RECEIVE_CONNECTION"], ev3.connected)
    elif whatToSend == "all":
        client.publish(topics["APP_REQUEST"], "thread")
        client.publish(topics["APP_REQUEST"], "locked")
        client.publish(topics["APP_REQUEST"], "pending")
        client.publish(topics["APP_REQUEST"], "waiting")
        client.publish(topics["APP_REQUEST"], "actions")
        client.publish(topics["APP_REQUEST"], "connection")

def onAppRequestImg(client, ev3, msg, controller):
    # cap = cv2.VideoCapture(0)
    # while True:
    #     retval, img = cap.read()
    #     if img is not None:
    #         img = cv2.flip(img, 1)
    #         retval, buffer = cv2.imencode('.jpg', img)
    #         jpg = base64.b64encode(buffer)
    #         client.publish(topics["APP_RECEIVE_IMG"], jpg)
    #         cap.release()
    #         break
    global va
    img = va.getFrame()
    retval, buffer = cv2.imencode('.jpg', img)
    jpg = base64.b64encode(buffer)
    client.publish(topics["APP_RECEIVE_IMG"], jpg)

def onPrintStates(client, ev3, msg, controller):
    print("> These are the current execution threads: ")
    for tag in controller.actionQueues:
        print("{0} => {1} with actions:".format(
            tag,
            controller.actionQueues[tag].state),
            controller.actionQueues[tag])

def onPrintPositions(client, ev3, msg, controller):
    print("> These are the current positions: ")
    ev3.publish(topics["EV3_PRINT_POS"])

def onEV3Connected(client, ev3, msg, controller):
    print("> EV3 Connected")
    ev3.publish(topics["APP_EV3_CONNECTED"])

def onAppSaveEV11IP(client, ev3, msg, controller):
    config = json.load(open(configPath))
    ip = msg.payload.decode()
    config["ips"]["INF_11"] = ip
    with open(configPath, 'w') as out:
        json.dump(config, out)
    ev3.setDisconnected("11")
    ev3.client11.disconnect()

    print("> EV3 INF_11 IP rewritten to {0}".format(ip))

def onAppSaveEV31IP(client, ev3, msg, controller):
    config = json.load(open(configPath))
    ip = msg.payload.decode()
    config["ips"]["INF_31"] = ip
    with open(configPath, 'w') as out:
        json.dump(config, out)

    ev3.setDisconnected("31")
    ev3.client31.disconnect()
    print("> EV3 INF_31 IP rewritten to {0}".format(ip))

def onAppConn(client, ev3, msg, controller):
    print("> App wants to connect to the controller!")
    client.publish(topics["CONN_ACK"])

def onAppRequestBoxes(client, ev3, msg, controller):
    boxes = generateRandBoxes()
    sa = StackingAlgorithm(boxes,(20,20),'BPOF')
    # have to adapt the sorted boxes
    # into something parseable by JSON
    # now send the app the sortedBoxes
    sortedBoxes = adaptPackingBoxes(sa.packer.bins)
    client.publish(topics["APP_RECEIVE_BOXES"], json.dumps(sortedBoxes))

def adaptPackingBoxes(bins):
    sortedBoxes = []
    lvl = -1
    for bin in bins:
        sortedBin = []
        lvl += 1
        for box in bin.boxes_packed:
            # we need color, length, width, height, and centreTo
            # invert if we rotate the box
            length = box.length
            width = box.width

            sBox = {
                "height": 4,
                "width": box.width * 2,
                "depth": box.length * 2,
                "color": box.colour,
                "x": (box.centreto[0] - (box.width / 2)) * 2,
                "y": lvl * 4,
                "z": (box.centreto[1] - (box.length / 2)) * 2
            }
            print(sBox)
            sortedBin.append(sBox)
        sortedBoxes.append(sortedBin)
    return sortedBoxes

def generateRandBoxes():
    numOfBoxes = randrange(20, 100)
    numOfBoxesForColor = numOfBoxes / 5
    boxes = []
    colours = ['red', 'blue', 'green', 'yellow', 'purple']
    for iteration in range(5):
        for i in range(int(numOfBoxesForColor)):
            boxes.append({
                "colour": colours[iteration],
                "centroid": (i+1, i+1),
                "rotation": 0,
                "width": randrange(1, 10),
                "length": randrange(1, 10)
            })
    return boxes
