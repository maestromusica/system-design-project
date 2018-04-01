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
  receivedBoxes,
  receiveVisionBoxes,
  receiveVisionState,
  appReceiveImg,
  boxSortCompleted,
  disableConnection,
  resetMiddleware,
  resetVisionState
} from './actions'

const initClient = (client, dispatch, state) => {
  console.log("INIT CALLED")
  // dispatch(saveClient(client))
  dispatch(clientDisconnected())
  dispatch(resetMiddleware())
  dispatch(resetVisionState())

  client.on('connect', () => {
    console.log("on connect called")
    client.subscribe(topics.APP_RECEIVE_THREAD)
    client.subscribe(topics.APP_RECEIVE_LOCKED)
    client.subscribe(topics.APP_RECEIVE_PENDING)
    client.subscribe(topics.APP_RECEIVE_WAITING)
    client.subscribe(topics.APP_RECEIVE_ACTIONS)
    client.subscribe(topics.APP_RECEIVE_CONNECTION)
    client.subscribe(topics.APP_RECEIVE_BOXES)
    client.subscribe(topics.APP_RECEIVE_IMG)
    client.subscribe(topics.APP_RECEIVE_VISION_STATE)
    client.subscribe(topics.APP_RECEIVE_VISION_BOXES)
    client.subscribe(topics.BOX_SORT_COMPLETED)
    client.subscribe(topics.CONN_ACK)
    client.subscribe(topics.CONN_DISABLE)

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
        console.log(data)
        dispatch(appReceiveThread(data))
        break
      case topics.APP_RECEIVE_LOCKED:
        dispatch(appReceiveLocked(data == "true"))
        break
      case topics.APP_RECEIVE_PENDING:
        dispatch(appReceivePending(data == "true"))
        break
      case topics.APP_RECEIVE_WAITING:
        dispatch(appReceiveWaiting(data == "true"))
        break
      case topics.APP_RECEIVE_ACTIONS:
        dispatch(appReceiveActions(JSON.parse(data)))
        break
      case topics.APP_RECEIVE_CONNECTION:
        dispatch(appReceiveEV3Connection(data == "true"))
        break
      case topics.CONN_ACK:
        dispatch(clientConnected())
        client.publish(topics.APP_REQUEST, "all")
        dispatch(resetVisionState())
        break
      case topics.APP_RECEIVE_BOXES:
        dispatch(receivedBoxes(JSON.parse(data)))
        break
      case topics.APP_RECEIVE_IMG:
        dispatch(appReceiveImg(data))
        break
      case topics.APP_RECEIVE_VISION_BOXES:
        dispatch(receiveVisionBoxes(JSON.parse(data)))
        break
      case topics.APP_RECEIVE_VISION_STATE:
        console.log("Connection", data)
        dispatch(receiveVisionState(data == "true"))
        break
      case topics.BOX_SORT_COMPLETED:
        dispatch(boxSortCompleted())
        break
      case topics.CONN_DISABLE:
        dispatch(disableConnection())
        dispatch(resetVisionState())
        dispatch(resetMiddleware())
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
