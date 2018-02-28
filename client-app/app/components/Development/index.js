import React, {Component} from 'react'
import topics from '../../../../topics.json' // this is an ugly path...
import mqtt from 'mqtt'

const LOCALHOST_IP = "mqtt://127.0.0.1"

export default class Development extends Component {
  state = {
    client: mqtt.connect(LOCALHOST_IP),
    thread: undefined
  }

  componentDidMount() {
    this.state.client.on('connect', () => {
      this.state.client.subscribe(topics.APP_RECIEVE_THREAD)
      this.state.client.publish(topics.APP_REQUEST_THREAD)
    })

    this.state.client.on('message', (topic, message) => {
      if(topic == topics.APP_RECIEVE_THREAD) {
        this.setState({
          thread: message.toString()
        })
      }
    })
  }

  render() {
    return (
      <div>
        {!this.state.thread ? (
          null
        ) : (
          <p>on thread {this.state.thread}</p>
        ) }
        <p>MoveX</p>
        <input onChange={ev => {
          this.setState({
            moveX: ev.target.value
          })
        }}  placeholder="moveX" />
        <button onClick={ev => {
          this.state.client.publish(topics.CONTROLLER_MOVE_X, this.state.moveX)
        }}>Send command</button>
        <p>MoveY</p>
        <input onChange={ev => {
          this.setState({
            moveY: ev.target.value
          })
        }}  placeholder="moveY" />
        <button onClick={ev => {
          this.state.client.publish(topics.CONTROLLER_MOVE_Y, this.state.moveY)
        }}>Send command</button>
        <p>MoveZ</p>
        <input onChange={ev => {
          this.setState({
            moveZ: ev.target.value
          })
        }}  placeholder="moveZ" />
        <button onClick={ev => {
          this.state.client.publish(topics.CONTROLLER_MOVE_Z, this.state.moveZ)
        }}>Send command</button>
      </div>
    )
  }
}
