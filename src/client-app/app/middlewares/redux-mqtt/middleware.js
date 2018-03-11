import mqtt from 'mqtt'
import {topics} from '../../utils/config'
import {
  clientConnected,
  clientDisconnected,
  ev3Connected,
  appReceiveThread,
  appReceiveLocked,
  appReceivePending,
  appReceiveActions
} from './actions'

const reduxMqttMiddleware = ip => ({dispatch}) => {
  const client = mqtt.connect(ip)

  client.on('connect', () => {
    client.subscribe(topics.APP_EV3_CONNECTED)
    client.subscribe(topics.APP_RECEIVE_THREAD)
    client.subscribe(topics.APP_RECEIVE_LOCKED)
    client.subscribe(topics.APP_RECEIVE_PENDING)
    client.subscribe(topics.APP_RECEIVE_WAITING)
    client.subscribe(topics.APP_RECEIVE_ACTIONS)

    client.publish(topics.APP_REQUEST, "all")
    dispatch(clientConnected())
  })

  client.on('disconnect', () => {
    dispatch(clientDisconnected())
  })

  client.on('message', (topic, msg) => {
    console.log("mata", topic)
    const data = msg.toString()
    switch(topic) {
      case topics.APP_EV3_CONNECTED:
        dispatch(ev3Connected())
        break
      case topics.APP_RECEIVE_THREAD:
        dispatch(appReceiveThread(data))
        break
      case topics.APP_RECEIVE_LOCKED:
        dispatch(appReceiveLocked(data))
        break
      case topic.APP_RECEIVE_PENDING:
        dispatch(appReceivePending(data))
        break
      case topics.APP_RECEIVE_ACTIONS:
        dispatch(appReceiveActions(data))
        break
    }
  })

  return next => (action) => {
    if(action.topic) {
      console.log('next action', action)
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
