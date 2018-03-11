import {topics} from '../../../utils/config'

export const CLIENT_CONNECTED = 'CLIENT_CONNECTED'
export const EV3_CONNECTED = 'EV3_CONNECTED'
export const CLIENT_DISCONNECTED = 'CLIENT_DISCONNECTED'
export const EV3_DISCONNECTED = 'EV3_DISCONNECTED'

export const clientConnected = () => ({
  type: CLIENT_CONNECTED
})

export const clientDisconnected = () => ({
  type: CLIENT_DISCONNECTED
})

export const ev3Connected = () => ({
  type: EV3_CONNECTED
})

export const ev3Disconnected = () => ({
  type: EV3_DISCONNECTED
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

export const appReceiveActions = data => ({
  type: topics.APP_RECEIVE_ACTIONS,
  data: {
    actions: JSON.parse(data)
  }
})
