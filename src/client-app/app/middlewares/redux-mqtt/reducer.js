import {
  CLIENT_CONNECTED,
  CLIENT_DISCONNECTED,
  SAVE_CLIENT
} from './actions'
import {topics} from '../../utils/config'

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
  ev3Connected: false,
  client: undefined
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
        connected: false,
        ev3Connected: false
      }
    case topics.APP_RECEIVE_CONNECTION:
      return {
        ...state,
        ev3Connected: action.data.connected
      }
    case SAVE_CLIENT:
      return {
        ...state,
        client: action.data.client
      }
    default:
      return state
  }
}

export default {
  meta,
  thread
}
