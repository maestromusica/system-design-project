import React, {Component} from 'react'
import mqtt from 'mqtt'
import topics from '../../../../topics.json' // this is an ugly path...

const LOCALHOST_IP = 'mqtt://127.0.0.1'

export default class LifecycleButton extends Component {
  state = {
    started: false,
    client: mqtt.connect(LOCALHOST_IP)
  }

  constructor(props) {
    super(props)
    this.state.client.on('connect', () => {
      console.log('client connected')
    })
  }

  _onClick = (ev) => {
    this.state.client.publish(topics.START_CONTROLLER)
  }

  render() {
    return (
      <button onClick={this._onClick}>Send message</button>
    )
  }
}
