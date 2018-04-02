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
    controller.sorting = False
    controller.sortedBoxes = []
    client.publish(topics["CONTROLLER_DELETE"], "all")
    client.publish(topics["APP_REQUEST_IMG"])
    sendData("executionQueue", client, controller, ev3)
    sendData("vision", client, controller, ev3)
    sendData("visionBoxes", client, controller, ev3)

def onProcessResponse(client, ev3, msg, controller):
    if msg.payload.decode() == "True":
        #visionActionQueue = controller.actionQueues[visionTag]
        #quantitative1(visionActionQueue)

        # Populate the queue.
        global va
        bins = va.execute()
        sortedBoxes = adaptPackingBoxes(bins)
        controller.sortedBoxes = sortedBoxes
        controller.sorting = True

        sendData("visionBoxes", client, controller, ev3)
        sendData("vision", client, controller, ev3)
        sendData("actions", client, controller, ev3)
        print(controller.actionQueues[visionTag])
        print("> Accepted")
    elif msg.payload.decode() == "False":
        controller.sorting = False
        controller.sortedBoxes = []
        sendData("vision", client, controller, ev3)
        sendData("visionBoxes", client, controller, ev3)
        print("> Not accepted")

def onSwitchExecutionThread(client, ev3, msg, controller):
    tag = msg.payload.decode()
    switched = controller.changeExecutionQueue(tag)
    if switched:
        print("> Execution thread switched to {0}".format(tag))
        sendData("executionQueue", client, controller, ev3)
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
    sendData("pending", client, controller, ev3)

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
    sendData("pending", client, controller, ev3)

def forwardAction(action):
    def curriedForwardedAction(client, ev3, msg, controller):
        controller.changeExecutionQueue(controllerTag)
        payload = msg.payload.decode()
        controller.actionQueues[controllerTag].put({
            "action": action,
            "payload": payload
        })
        currentExecThread = controller.currentExecutionThread()
        if currentExecThread.state.pending:
            ev3.publish(topics["EV3_REQUEST_NEXT"])
        print("> Next action added to the queue")
        sendData("executionQueue", client, controller, ev3)

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
        sendData("actions", client, controller, ev3)
        return
    else:
        # asusmed it's an integer
        pos = int(payload)

    if pos >= 0 and pos < len(currentExecThread):
        removed = currentExecThread.remove(pos)
        if removed == None:
            print("> Action was not deleted!")
        else:
            print("> Action was deleted.")
    else:
        print("Positional argument is not within queue boundary")
        return
    sendData("actions", client, controller, ev3)

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

def sendData(whatToSend, client, controller, ev3):
    currentExecThread = controller.currentExecutionThread()
    if whatToSend == "thread":
        client.publish(topics["APP_RECEIVE_THREAD"], controller.currentExecThreadTag)
    elif whatToSend == "locked":
        client.publish(topics["APP_RECEIVE_LOCKED"], json.dumps(currentExecThread.state.locked))
    elif whatToSend == "pending":
        client.publish(topics["APP_RECEIVE_PENDING"], json.dumps(currentExecThread.state.pending))
    elif whatToSend == "waiting":
        client.publish(topics["APP_RECEIVE_WAITING"], json.dumps(currentExecThread.state.waiting))
    elif whatToSend == "actions":
        actions = numpy.array(currentExecThread.queue).tolist()
        client.publish(topics["APP_RECEIVE_ACTIONS"], json.dumps(actions))
    elif whatToSend == "connection":
        client.publish(topics["APP_RECEIVE_CONNECTION"], json.dumps(ev3.connected))
    elif whatToSend == "vision":
        client.publish(topics["APP_RECEIVE_VISION_STATE"], json.dumps(controller.sorting))
    elif whatToSend == "visionBoxes":
        client.publish(topics["APP_RECEIVE_VISION_BOXES"], json.dumps(controller.sortedBoxes))
    elif whatToSend == "executionQueue":
        sendData("thread", client, controller, ev3)
        sendData("locked", client, controller, ev3)
        sendData("pending", client, controller, ev3)
        sendData("waiting", client, controller, ev3)
        sendData("actions", client, controller, ev3)
        sendData("vision", client, controller, ev3)
    elif whatToSend == "all":
        sendData("thread", client, controller, ev3)
        sendData("locked", client, controller, ev3)
        sendData("pending", client, controller, ev3)
        sendData("waiting", client, controller, ev3)
        sendData("actions", client, controller, ev3)
        sendData("connection", client, controller, ev3)
        sendData("vision", client, controller, ev3)
        sendData("visionBoxes", client, controller, ev3)
    else:
        raise Error()

def onAppRequestData(client, ev3, msg, controller):
    whatToSend = msg.payload.decode()
    currentExecThread = controller.currentExecutionThread()
    sendData(whatToSend, client, controller, ev3)

def onAppRequestImg(client, ev3, msg, controller):
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
    sendData("connection", client, controller, ev3)

def onAppSaveEV31IP(client, ev3, msg, controller):
    config = json.load(open(configPath))
    ip = msg.payload.decode()
    config["ips"]["INF_31"] = ip
    with open(configPath, 'w') as out:
        json.dump(config, out)

    ev3.setDisconnected("31")
    ev3.client31.disconnect()
    print("> EV3 INF_31 IP rewritten to {0}".format(ip))
    sendData("connection", client, controller, ev3)

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
            print("Box: ", box.colour)
            # we need color, length, width, height, and centreTo
            # invert if we rotate the box
            length = box.length
            width = box.width

            sBox = {
                "width": box.width,
                "length": box.length,
                "colour": box.colour,
                "centreto": box.centreto.tolist()
            }
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

def onResumeSorting(client, ev3, msg, controller):
    controller.changeExecutionQueue(visionTag)
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.state.pending = True
    currentExecThread.state.locked = False
    client.publish(topics["RESUME_CONTROLLER"])
    sendData("executionQueue", client, controller, ev3)

def onPauseSorting(client, ev3, msg, controller):
    controller.changeExecutionQueue(visionTag)
    client.publish(topics["STOP_CONTROLLER"])
    sendData("executionQueue", client, controller, ev3)

def onEndSorting(client, ev3, msg, controller):
    controller.changeExecutionQueue(visionTag)
    currentExecThread = controller.currentExecutionThread()
    currentExecThread.state.locked = True
    controller.sorting = False
    controller.sortedBoxes = []
    client.publish(topics["CONTROLLER_DELETE"], "all")
    sendData("thread", client, controller, ev3)
    sendData("pending", client, controller, ev3)
    sendData("waiting", client, controller, ev3)
    sendData("locked", client, controller, ev3)
    sendData("vision", client, controller, ev3)
    sendData("visionBoxes", client, controller, ev3)
    # don't send actions because we previously send to delete all acitons
    # let that function send the app the action Queue
