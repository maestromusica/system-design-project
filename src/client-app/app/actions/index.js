import {topics} from '../utils/config'
import {initClient} from '../middlewares/redux-mqtt/middleware'
import {clientDisconnected} from '../middlewares/redux-mqtt/actions'

const FORWARD_TO_MQTT = "forward_to_mqtt"

export const deleteAction = (pos) => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_DELETE,
  data: pos
})

export const requestNextAction = () => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_NEXT_ACTION
})

export const moveX = (pos) => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_MOVE_X,
  data: pos
})

export const moveY = (pos) => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_MOVE_Y,
  data: pos
})

export const moveZ = (pos) => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_MOVE_Z,
  data: pos
})

export const grab = (pos) => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_GRAB,
  data: pos
})

export const rotate = (pos) => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_ROTATE,
  data: pos
})

export const resetX = () => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_RESET_X,
})

export const resetY = () => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_RESET_Y
})

export const resetZ = () => ({
  type: FORWARD_TO_MQTT,
  topic: topics.CONTROLLER_RESET_Z
})

export const switchExecutionThread = thread => ({
  type: FORWARD_TO_MQTT,
  topic: topics.SWITCH_CONTROLLER_EXEC,
  data: thread
})

export const resumeController = () => ({
  type: FORWARD_TO_MQTT,
  topic: topics.RESUME_CONTROLLER
})

export const stopController = () => ({
  type: FORWARD_TO_MQTT,
  topic: topics.STOP_CONTROLLER
})

export const switchExecToNotPending = () => ({
  type: FORWARD_TO_MQTT,
  topic: topics.SWITCH_EXEC_NOT_PENDING
})

export const switchExecToPending = () => ({
  type: FORWARD_TO_MQTT,
  topic: topics.SWITCH_EXEC_PENDING
})

export const addControllerIP = ip => ({
  type: 'ADD_CONTROLLER_IP',
  ip: ip,
})

export const add11IP = ip => ({
  type: 'ADD_11_IP',
  topic: topics.CONTROLLER_SAVE_IP_11,
  ip: ip,
  data: ip // need for forwarding mqtt
})

export const add31IP = ip => ({
  type: 'ADD_31_IP',
  topic: topics.CONTROLLER_SAVE_IP_31,
  ip: ip,
  data: ip // need for forwarding mqtt
})

export const restartClient = () => {
  return (dispatch, getState) => {
    dispatch(clientDisconnected())
    dispatch({type: "RESTART_CLIENT"})
  }
}

export const connectEV3 = () => ({
  type: topics.APP_CONNECT_EV3,
  topic: topics.APP_CONNECT_EV3
})

export const requestBoxes = () => ({
  type: topics.APP_REQUEST_BOXES,
  topic: topics.APP_REQUEST_BOXES
})
