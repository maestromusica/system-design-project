export const MQTT_IP = "mqtt://127.0.0.1"
export const topics = {
    "START_CONTROLLER": "action/controller/start",
    "PROCESS_CONTROLLER": "action/controller/process",
    "PROCESS_RESPONSE_CONTROLLER": "action/controller/process/res",
    "PROCESS_CONTROLLER_ID": "action/controller/process/add/id",
    "CONTROLLER_DELETE": "action/controller/delete/exec/action",

    "STOP_CONTROLLER": "action/controller/stop/ev3",
    "RESUME_CONTROLLER": "action/controller/resume/ev3",
    "PAUSE_CONTROLLER": "action/controller/pause/ev3",
    "SWITCH_CONTROLLER_EXEC": "action/controller/switch/exec",
    "SWITCH_EXEC_PENDING": "action/controller/switch/exec/p",
    "SWITCH_EXEC_NOT_PENDING": "action/controller/switch/exec/np",

    "QUIT_CONTROLLER": "action/controller/quit",
    "CONTROLLER_PRINT_STATES": "action/controller/print/states",
    "CONTROLLER_PRINT": "action/controller/print",
    "CONTROLLER_PRINT_POS": "action/controller/print/pos",
    "CONTROLLER_NEXT_ACTION": "action/controller/exec/next",

    "CONTROLLER_MOVE_X": "action/controller/move/x",
    "CONTROLLER_MOVE_Y": "action/controller/move/y",
    "CONTROLLER_MOVE_Z": "action/controller/move/z",
    "CONTROLLER_GRAB": "action/controller/move/grab",
    "CONTROLLER_RELEASE": "action/controller/move/release",
    "CONTROLLER_ROTATE": "action/controller/move/rotate",
    "CONTROLLER_RESET_X": "action/controller/reset/x",
    "CONTROLLER_RESET_Y": "action/controller/reset/y",
    "CONTROLLER_RESET_Z": "action/controller/reset/z",

    "EV3_STOP": "action/ev3/stop",
    "EV3_RESUME": "action/ev3/resume",
    "EV3_PAUSE": "action/ev3/pause",

    "EV3_ACTION_COMPLETED": "inform/ev3/action/completed",
    "EV3_REQUEST_NEXT": "request/ev3/next/action",
    "EV3_MOVE_X": "action/ev3/move/x",
    "EV3_MOVE_Y": "action/ev3/move/y",
    "EV3_MOVE_Z": "action/ev3/move/z",
    "EV3_MOVE_GRAB": "action/ev3/move/grab",
    "EV3_MOVE_RELEASE": "action/ev3/move/release",
    "EV3_ROTATE": "action/ev3/move/rotate",
    "EV3_RESET_X": "action/ev3/reset/x",
    "EV3_RESET_Y": "action/ev3/reset/y",
    "EV3_RESET_Z": "action/ev3/reset/z",

    "EV3_PRINT_POS": "action/ev3/forward/print/pos",

    "APP_REQUEST": "action/app/request/data",

    "APP_RECEIVE_POS": "action/app/receive/data/pos",
    "APP_RECEIVE_THREAD": "action/app/receive/data/thread",
    "APP_RECEIVE_LOCKED": "action/app/receive/data/locked",
    "APP_RECEIVE_PENDING": "action/app/receive/data/pending",
    "APP_RECEIVE_WAITING": "action/app/receive/data/waiting",
    "APP_RECEIVE_ACTIONS": "action/app/receive/data/actions",
    "APP_RECEIVE_CONNECTION": "aciton/app/receive/data/connection",

    "APP_RECEIVE_IMG": "action/app/receive/data/video_feed",
    "APP_REQUEST_IMG": "action/app/request/data/video_feed",
    "APP_REQUEST_BOXES": "action/app/request/data/boxes",
    "APP_RECEIVE_BOXES": "/action/app/receive/data/sorted_boxes",
    "APP_RECEIVE_VISION_BOXES": "/action/app/receive/data/vision_boxes",
    "APP_RECEIVE_VISION_STATE": "/action/app/receive/data/vision/state",

    "CONTROLLER_SAVE_IP_11": "config/app/save/ip/INF_11",
    "CONTROLLER_SAVE_IP_31": "config/app/save/ip/INF_31",

    "APP_CONNECT_EV3": "action/app/connect/ev3",

    "EV3_CONNECTED": "info/ev3/connected",
    "APP_EV3_CONNECTED": "info/app/ev3/connected",

    "CONN": "info/controller/check/connection",
    "CONN_ACK": "info/controller/ack/connection",
    "CONN_DISABLE": "info/controller/disable/connection",
    "EV3_CONN": "info/ev3/check/connection",
    "EV3_CONN_ACK": "info/ev3/ack/connection",

    "BOX_SORT_COMPLETED": "info/controller/sort/completed",
    "RESUME_SORTING": "action/controller/resume/sort",
    "PAUSE_SORTING": "action/controller/pause/sort",
    "END_SORTING": "action/controller/end/sort"
}


// export {default as topics} from '../../../config/topics.json'
