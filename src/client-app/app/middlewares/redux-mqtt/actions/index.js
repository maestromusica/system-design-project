import {topics} from '../../../utils/config'

export const CLIENT_CONNECTED = 'CLIENT_CONNECTED'
export const CLIENT_DISCONNECTED = 'CLIENT_DISCONNECTED'
export const SAVE_CLIENT = 'SAVE_CLIENT'
export const RESET_MIDDLEWARE = 'RESET_MIDDLEWARE'
export const RESET_VISION_STATE = 'RESET_VISION_STATE'

export const clientConnected = () => ({
  type: CLIENT_CONNECTED
})

export const clientDisconnected = () => ({
  type: CLIENT_DISCONNECTED
})

export const appReceiveEV3Connection = data => ({
  type: topics.APP_RECEIVE_CONNECTION,
  data: {
    connected: data
  }
})

export const appReceiveThread = data => ({
  type: topics.APP_RECEIVE_THREAD,
  data: {
    name: data
  }
})

export const appReceiveLocked = data => ({
  type: topics.APP_RECEIVE_LOCKED,
  data: {
    locked: data
  }
})

export const appReceivePending = data => ({
  type: topics.APP_RECEIVE_PENDING,
  data: {
    pending: data
  }
})

export const appReceiveWaiting = data => ({
  type: topics.APP_RECEIVE_WAITING,
  data: {
    waiting: data
  }
})

export const appReceiveActions = data => ({
  type: topics.APP_RECEIVE_ACTIONS,
  data: {
    actions: data
  }
})

export const saveClient = client => ({
  type: "SAVE_CLIENT",
  data: {
    client: client
  }
})

export const receivedBoxes = data => ({
  type: topics.APP_RECEIVE_BOXES,
  data: {
    boxes: data
  }
})

export const receiveVisionBoxes = data => ({
  type: topics.APP_RECEIVE_VISION_BOXES,
  data: {
    boxes: data.boxes,
    id: data.id
  }
})

export const receiveVisionState = data => ({
  type: topics.APP_RECEIVE_VISION_STATE,
  data: {
    sorting: data
  }
})

export const appReceiveImg = data => ({
  type: topics.APP_RECEIVE_IMG,
  data: {
    img: data,
    waiting: false
  }
})

export const boxSortCompleted = () => ({
  type: topics.BOX_SORT_COMPLETED
})

export const disableConnection = () => ({
  type: topics.CONN_DISABLE
})

export const resetMiddleware = () => ({
  type: RESET_MIDDLEWARE
})

export const resetVisionState = () => ({
  type: RESET_VISION_STATE
})
