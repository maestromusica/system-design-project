import {topics} from '../../../utils/config'

export const CLIENT_CONNECTED = 'CLIENT_CONNECTED'
export const CLIENT_DISCONNECTED = 'CLIENT_DISCONNECTED'
export const SAVE_CLIENT = 'SAVE_CLIENT'

export const clientConnected = () => ({
  type: CLIENT_CONNECTED
})

export const clientDisconnected = () => ({
  type: CLIENT_DISCONNECTED
})

export const appReceiveEV3Connection = data => ({
  type: topics.APP_RECEIVE_CONNECTION,
  data: {
    connected: data == "True"
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
    locked: data === "True"
  }
})

export const appReceivePending = data => ({
  type: topics.APP_RECEIVE_PENDING,
  data: {
    pending: data === "True"
  }
})

export const appReceiveWaiting = data => ({
  type: topics.APP_RECEIVE_WAITING,
  data: {
    waiting: data === "True"
  }
})

export const appReceiveActions = data => ({
  type: topics.APP_RECEIVE_ACTIONS,
  data: {
    actions: JSON.parse(data)
  }
})

export const saveClient = client => ({
  type: "SAVE_CLIENT",
  data: {
    client: client
  }
})
