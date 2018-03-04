import React, {Component} from 'react'
import topics from '../../../../topics.json' // this is an ugly path...
import mqtt from 'mqtt'
import ThreadSection from './ThreadSection'
import AxisSection from './AxisSection'
import ResetSection from './ResetSection'
import ActionsSection from './ActionsSection'

const LOCALHOST_IP = "mqtt://127.0.0.1"

export default class Development extends Component {
  state = {
    client: mqtt.connect(LOCALHOST_IP),
    thread: undefined,
    threadLocked: undefined,
    threadPending: undefined,
    actions: []
  }

  componentDidMount() {
    this.state.client.on('connect', () => {
      this.state.client.subscribe(topics.APP_RECIEVE_THREAD)
      this.state.client.subscribe(topics.APP_RECIEVE_LOCKED)
      this.state.client.subscribe(topics.APP_RECIEVE_PENDING)
      this.state.client.subscribe(topics.APP_RECIEVE_ACTIONS)

      this.state.client.publish(topics.APP_REQUEST, "all")
    })

    this.state.client.on('message', (topic, message) => {
      console.log(topic, message)
      switch(topic) {
        case topics.APP_RECIEVE_THREAD:
          this.setState({
            thread: message.toString()
          })
          break
        case topics.APP_RECIEVE_LOCKED:
          this.setState({
            threadLocked: message.toString() === "True"
          })
          break
        case topics.APP_RECIEVE_PENDING:
          this.setState({
            threadPending: message.toString() === "True"
          })
          break
        case topics.APP_RECIEVE_ACTIONS:
          this.setState({
            actions: JSON.parse(message.toString())
          })
          break
      }
    })
  }

  componentWillUnmount() {
    const forceEnd = true
    this.state.client.end(forceEnd)
  }

  render() {
    return (
      <div>
        <ThreadSection
          client={this.state.client}
          thread={this.state.thread}
          threadPending={this.state.threadPending}
          threadLocked={this.state.threadLocked}
        />
        <AxisSection
          client={this.state.client}
        />
        <ResetSection
          client={this.state.client}
        />
        <ActionsSection
          client={this.state.client}
          threadPending={this.state.threadPending}
          actions={this.state.actions}
        />
      </div>
    )
  }
}
