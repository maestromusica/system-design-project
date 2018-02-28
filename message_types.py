import json

topics = json.load(open("topics.json"))

class Topics:
    START_CONTROLLER = topics["START_CONTROLLER"]
    PROCESS_CONTROLLER = topics["PROCESS_CONTROLLER"]
    CONTROLLER_DELETE = topics["CONTROLLER_DELETE"]
    # acts upon the ev3s (and the controller execution thread)
    STOP_CONTROLLER = topics["STOP_CONTROLLER"]
    RESUME_CONTROLLER = topics["RESUME_CONTROLLER"]
    PAUSE_CONTROLLER = topics["PAUSE_CONTROLLER"]
    SWITCH_CONTROLLER_EXEC = topics["SWITCH_CONTROLLER_EXEC"]
    SWITCH_EXEC_PENDING = topics["SWITCH_EXEC_PENDING"]
    SWITCH_EXEC_NOT_PENDING = topics["SWITCH_EXEC_NOT_PENDING"]
    # QUIT_CONTROLLER = createTopicString("action/controller/quit")
    CONTROLLER_PRINT_STATES = topics["CONTROLLER_PRINT_STATES"]
    CONTROLLER_PRINT = topics["CONTROLLER_PRINT"]
    CONTROLLER_PRINT_POS = topics["CONTROLLER_PRINT_POS"]
    CONTROLLER_NEXT_ACTION = topics["CONTROLLER_NEXT_ACTION"]

    # the client sends these and the controller forwards them
    CONTROLLER_MOVE_X = topics["CONTROLLER_MOVE_X"]
    CONTROLLER_MOVE_Y = topics["CONTROLLER_MOVE_Y"]
    CONTROLLER_MOVE_Z = topics["CONTROLLER_MOVE_Z"]
    CONTROLLER_GRAB = topics["CONTROLLER_GRAB"]
    CONTROLLER_RELEASE = topics["CONTROLLER_RELEASE"]
    CONTROLLER_RESET_X = topics["CONTROLLER_RESET_X"]
    CONTROLLER_RESET_Y = topics["CONTROLLER_RESET_Y"]
    CONTROLLER_RESET_Z = topics["CONTROLLER_RESET_Z"]

    # ev3 lifecycle related
    EV3_STOP = topics["EV3_STOP"]
    EV3_RESUME = topics["EV3_RESUME"]
    EV3_PAUSE = topics["EV3_PAUSE"]

    # ev3 action related
    EV3_ACTION_COMPLETED = topics["EV3_ACTION_COMPLETED"]
    EV3_REQUEST_NEXT = topics["EV3_REQUEST_NEXT"]
    EV3_MOVE_X = topics["EV3_MOVE_X"]
    EV3_MOVE_Y = topics["EV3_MOVE_Y"]
    EV3_MOVE_Z = topics["EV3_MOVE_Z"]
    EV3_MOVE_GRAB = topics["EV3_MOVE_GRAB"]
    EV3_MOVE_RELEASE = topics["EV3_MOVE_RELEASE"]
    EV3_RESET_X = topics["EV3_RESET_X"]
    EV3_RESET_Y = topics["EV3_RESET_Y"]
    EV3_RESET_Z = topics["EV3_RESET_Z"]

    EV3_PRINT_POS = topics["EV3_PRINT_POS"]
