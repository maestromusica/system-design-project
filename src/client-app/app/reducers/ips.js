const defaultIpState = {
  CLIENT: '',
  INF_11: '',
  INF_31: ''
}

export default function ips(state = defaultIpState, action) {
  switch(action.type) {
    case 'ADD_CONTROLLER_IP':
      return {
        ...state,
        CLIENT: action.ip
      }
    case 'ADD_11_IP':
      return {
        ...state,
        INF_11: action.ip
      }
    case 'ADD_31_IP':
      return {
        ...state,
        INF_31: action.ip
      }
    default:
      return state
  }
}
