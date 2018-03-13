import mqtt from 'mqtt'
import {topics, MQTT_IP} from '../../utils/config'
import {
  clientConnected,
  clientDisconnected,
  appReceiveEV3Connection,
  appReceiveThread,
  appReceiveLocked,
  appReceivePending,
  appReceiveWaiting,
  appReceiveActions,
  saveClient,
  receivedBoxes
} from './actions'

const initClient = (client, dispatch, state) => {
  console.log("INIT CALLED")
  // dispatch(saveClient(client))
  dispatch(clientDisconnected())

  client.on('connect', () => {
    console.log("on connect called")
    client.subscribe(topics.APP_RECEIVE_THREAD)
    client.subscribe(topics.APP_RECEIVE_LOCKED)
    client.subscribe(topics.APP_RECEIVE_PENDING)
    client.subscribe(topics.APP_RECEIVE_WAITING)
    client.subscribe(topics.APP_RECEIVE_ACTIONS)
    client.subscribe(topics.APP_RECEIVE_CONNECTION)
    client.subscribe(topics.APP_RECEIVE_BOXES)
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
      case topics.APP_RECEIVE_BOXES:
        dispatch(receivedBoxes(data))
        break
    }
  })
}

const reduxMqttMiddleware = () => ({dispatch, getState}) => {
  let state = getState()
  let client
  const ip = MQTT_IP
  client = state.ips.CLIENT
    ? mqtt.connect("mqtt://" + state.ips.CLIENT + ":1883")
    : mqtt.connect(ip + ":1883")

  initClient(client, dispatch, state)

  console.log(">>>>> Middleware initialised!")

  return next => action => {
    if(action.type == "RESTART_CLIENT") {
      console.log("restart client called!")
      state = getState()
      // should restart the client
      console.log("should be called")
      client = undefined
      client = state.ips.CLIENT
        ? mqtt.connect("mqtt://" + state.ips.CLIENT + ":1883")
        : mqtt.connect(ip + ":1883")

      initClient(client, dispatch, getState())
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

export {initClient}
export default reduxMqttMiddleware
