import {
  CLIENT_CONNECTED,
  CLIENT_DISCONNECTED,
  EV3_CONNECTED,
  EV3_DISCONNECTED
} from './actions'
import topics from '../../../../config/topics.json'

const initialState = {
  name: undefined,
  locked: undefined,
  pending: undefined,
  waiting: undefined,
  actions: []
}

const thread = (state = initialState, action) => {
  switch(action.type) {
    case topics.APP_RECEIVE_THREAD:
      return {
        ...state,
        name: action.data.name
      }
    case topics.APP_RECEIVE_LOCKED:
      return {
        ...state,
        locked: action.data.locked
      }
    case topics.APP_RECEIVE_PENDING:
      return {
        ...state,
        pending: action.data.pending
      }
    case topics.APP_RECEIVE_ACTIONS:
      return {
        ...state,
        actions: action.data.actions
      }
    case topics.APP_RECEIVE_WAITING:
      return {
        ...state,
        waiting: action.data.waiting
      }
    default:
      return state
  }
}

const metaInitialState = {
  connected: false,
  ev3Connected: false
}

const meta = (state = metaInitialState, action) => {
  switch(action.type) {
    case CLIENT_CONNECTED:
      return {
        ...state,
        connected: true
      }
    case CLIENT_DISCONNECTED:
      return {
        ...state,
        connected: false
      }
    case EV3_CONNECTED:
      return {
        ...state,
        ev3Connected: true
      }
    case EV3_DISCONNECTED:
      return {
        ...state,
        ev3Disconnected: false
      }
    default:
      return state
  }
}

export default {
  meta,
  thread
}
