import mqtt from 'mqtt'
import {topics} from '../../utils/config'
import {
  clientConnected,
  clientDisconnected,
  appReceiveEV3Connection,
  appReceiveThread,
  appReceiveLocked,
  appReceivePending,
  appReceiveWaiting,
  appReceiveActions
} from './actions'

let client

const restartClient = (dispatch, state) => {
  if(client && client.connected) {
    client.end(true)
  }

  client = state.ips.CLIENT
    ? mqtt.connect("mqtt://" + state.ips.CLIENT)
    : mqtt.connect(ip)

  console.log(">>>>> This is called!!!!")

  dispatch(clientDisconnected())
  client.on('connect', () => {
    console.log("on connect called")
    client.subscribe(topics.APP_RECEIVE_THREAD)
    client.subscribe(topics.APP_RECEIVE_LOCKED)
    client.subscribe(topics.APP_RECEIVE_PENDING)
    client.subscribe(topics.APP_RECEIVE_WAITING)
    client.subscribe(topics.APP_RECEIVE_ACTIONS)
    client.subscribe(topics.APP_RECEIVE_CONNECTION)
    client.subscribe(topics.CONN_ACK)

    client.publish(topics.CONN)
  })

  client.on('disconnect', () => {
    console.log("on disconnect called!")
    dispatch(clientDisconnected())
  })

  client.on('message', (topic, msg) => {
    const data = msg.toString()
    switch(topic) {
      case topics.APP_RECEIVE_THREAD:
        dispatch(appReceiveThread(data))
        break
      case topics.APP_RECEIVE_LOCKED:
        dispatch(appReceiveLocked(data))
        break
      case topics.APP_RECEIVE_PENDING:
        dispatch(appReceivePending(data))
        break
      case topics.APP_RECEIVE_WAITING:
        dispatch(appReceiveWaiting(data))
        break
      case topics.APP_RECEIVE_ACTIONS:
        dispatch(appReceiveActions(data))
        break
      case topics.APP_RECEIVE_CONNECTION:
        dispatch(appReceiveEV3Connection(data))
        break
      case topics.CONN_ACK:
        dispatch(clientConnected())
        client.publish(topics.APP_REQUEST, "all")
        break
    }
  })
}

const reduxMqttMiddleware = (ip) => ({dispatch, getState}) => {
  restartClient(dispatch, getState())

  return next => action => {
    if(action.type == "ADD_CONTROLLER_IP") {
      restartClient(dispatch, getState())
      console.log("should connect...")
    }

    if(action.topic) {
      Promise.resolve(
        client.publish(action.topic, action.data)
      ).then(next(action))
    }
    else {
      next(action)
    }
  }
}

export default reduxMqttMiddleware
