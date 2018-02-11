from enum import Enum

# TODO: instead of using hardcoded versioning, maybe we could import this from
# a config
version = "v0.0.1"

def createTopicString(*args):
    return "/".join(["api", version, *args])

class Topics:
    REQUEST_DATA_BOXES = createTopicString("request/data/boxes")
    RECIEVE_DATA_BOXES = createTopicString("response/data/boxes")

    RECIEVE_DATA_NEXT = createTopicString("response/data/next/action")
    REQUEST_DATA_NEXT = createTopicString("request/data/next/action")

    START_CONTROLLER = createTopicString("action/controller/start")
    STOP_CONTROLLER = createTopicString("action/controller/stop")

    STOP_EV3 = createTopicString("action/ev3/stop")

    EV3_MOVE_X = createTopicString("action/ev3/move/x")
    EV3_MOVE_Y = createTopicString("action/ev3/move/y")
    EV3_MOVE_Z = createTopicString("action/ev3/move/z")
    EV3_MOVE_GRAB = createTopicString("action/ev3/move/grab")
    EV3_MOVE_RELEASE = createTopicString("action/ev3/move/release")
