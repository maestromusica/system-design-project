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

const reduxMqttMiddleware = (ip) => ({dispatch, getState}) => {
  const state = getState()
  const client = state.ips.CLIENT
    ? mqtt.connect("mqtt://" + state.ips.CLIENT)
    : mqtt.connect(ip)

  client.on('connect', () => {
    client.subscribe(topics.APP_EV3_CONNECTED)
    client.subscribe(topics.APP_RECEIVE_THREAD)
    client.subscribe(topics.APP_RECEIVE_LOCKED)
    client.subscribe(topics.APP_RECEIVE_PENDING)
    client.subscribe(topics.APP_RECEIVE_WAITING)
    client.subscribe(topics.APP_RECEIVE_ACTIONS)
    client.subscribe(topics.APP_RECEIVE_CONNECTION)

    client.publish(topics.APP_REQUEST, "all")
    dispatch(clientConnected())
  })

  client.on('disconnect', () => {
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
    }
  })

  return next => (action) => {
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
