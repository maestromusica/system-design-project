from enum import Enum

# TODO: instead of using hardcoded versioning, maybe we could import this from
# a config
version = "v0.0.1"

def createTopicString(*args):
    return "/".join(["api", version, *args])

class Topics:
    REQUEST_DATA_BOXES = createTopicString("request/data/boxes")
    RECIEVE_DATA_BOXES = createTopicString("response/data/boxes")

    START_CONTROLLER = createTopicString("action/controller/start")
    STOP_CONTROLLER = createTopicString("action/controller/stop")

    STOP_EV3 = createTopicString("action/ev3/stop")
