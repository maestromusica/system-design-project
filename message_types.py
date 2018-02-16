# TODO: instead of using hardcoded versioning, maybe we could import this from
# a config
version = "v0.0.1"

def createTopicString(args):
    return "/".join(["api", version, args])

class Topics:
    REQUEST_DATA_BOXES = createTopicString("request/data/boxes")
    RECIEVE_DATA_BOXES = createTopicString("response/data/boxes")

    RECIEVE_DATA_NEXT = createTopicString("response/data/next/action")
    REQUEST_DATA_NEXT = createTopicString("request/data/next/action")

    START_CONTROLLER = createTopicString("action/controller/start")
    STOP_CONTROLLER = createTopicString("action/controller/stop")
    # QUIT_CONTROLLER = createTopicString("action/controller/quit")

    # the client sends these and the controller forwards them
    CONTROLLER_MOVE_X = createTopicString("action/controller/move/x")
    CONTROLLER_MOVE_Y = createTopicString("action/controller/move/y")
    CONTROLLER_MOVE_Z = createTopicString("action/controller/move/z")
    CONTROLLER_GRAB = createTopicString("action/controller/move/grab")
    CONTROLLER_RELEASE = createTopicString("action/controller/move/release")

    EV3_STOP = createTopicString("action/ev3/stop")
    EV3_RESUME = createTopicString("action/ev3/resume")
    EV3_FORCE_STOP = createTopicString("action/ev3/fstop")

    EV3_REQUEST_NEXT = createTopicString("request/ev3/next/action")
    EV3_MOVE_X = createTopicString("action/ev3/move/x")
    EV3_MOVE_Y = createTopicString("action/ev3/move/y")
    EV3_MOVE_Z = createTopicString("action/ev3/move/z")
    EV3_MOVE_GRAB = createTopicString("action/ev3/move/grab")
    EV3_MOVE_RELEASE = createTopicString("action/ev3/move/release")
