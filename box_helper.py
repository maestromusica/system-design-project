from message_types import Topics

def mockBoxes(actionQueue):
    boxes = [{
        "length": 100,
        "width": 200,
        "height": 40,
        "x": 10,
        "y": 40 }, {
        "length": 40,
        "width": 20,
        "height": 90,
        "x": 10,
        "y": 90
    }]

    boxLocations = [{
        "to": {"x": 180, "y": 200},
        "from": {"x": 100, "y": 300}},{
        "to": {"x": 300, "y": 400},
        "from": {"x": 100, "y": 100}
    }]

    for (i, box) in enumerate(boxes):
        box["from"] = boxLocations[i]["from"]
        box["to"] = boxLocations[i]["to"]

    for box in boxes:
        actionQueue.put({
            "action": Topics.EV3_MOVE_X,
            "payload": box["from"]["x"]
        })
        actionQueue.put({
            "action": Topics.EV3_MOVE_Y,
            "payload": box["from"]["y"]
        })
        actionQueue.put({
            "action": Topics.EV3_MOVE_GRAB,
            "payload": {}
        })
        actionQueue.put({
            "action": Topics.EV3_MOVE_X,
            "payload": box["to"]["x"]
        })
        actionQueue.put({
            "action": Topics.EV3_MOVE_Y,
            "payload": box["to"]["y"]
        })
        actionQueue.put({
            "action": Topics.EV3_MOVE_RELEASE,
            "payload": {}
        })
