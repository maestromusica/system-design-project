import {topics} from '../utils/config'

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
  topic: topics.SWTCH_EXEC_PENDING
})

export const addControllerIP = (ip) => ({
  type: FORWARD_TO_MQTT,
  type: 'ADD_CONTROLLER_IP',
  ip: ip
})
