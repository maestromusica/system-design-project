export default function ips(state = {}, action) {
  switch(action.type) {
    case 'ADD_CONTROLLER_IP':
      return {
        ...state,
        ip: action.ip
      }
    default:
      return state
  }
}
