import React, {Component} from 'react'
import topics from '../../../../topics.json' // this is an ugly path...
import mqtt from 'mqtt'
import {
  DevStyle,
  DevSection,
  DevSectionItem,
  DevSectionTitle,
  DevOption,
  DevOptionInput,
  DevOptionTitle,
  DevOptionButton} from './style'
import {Radio, Switch} from 'antd'
const RadioGroup = Radio.Group

const LOCALHOST_IP = "mqtt://127.0.0.1"

export default class Development extends Component {
  state = {
    client: mqtt.connect(LOCALHOST_IP),
    thread: undefined,
    threadLocked: undefined,
    threadPending: undefined
  }

  componentDidMount() {
    this.state.client.on('connect', () => {
      this.state.client.subscribe(topics.APP_RECIEVE_THREAD)
      this.state.client.subscribe(topics.APP_RECIEVE_LOCKED)
      this.state.client.subscribe(topics.APP_RECIEVE_PENDING)

      this.state.client.publish(topics.APP_REQUEST, "thread")
      this.state.client.publish(topics.APP_REQUEST,  "locked")
      this.state.client.publish(topics.APP_REQUEST, "pending")
    })

    this.state.client.on('message', (topic, message) => {
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
      }
    })
  }

  componentWillUnmount() {
    const forceEnd = true
    this.state.client.end(forceEnd)
  }

  render() {
    return (
      <DevStyle>
        <DevSection>
          <DevSectionItem>
            <DevSectionTitle>
              Thread
            </DevSectionTitle>
            <RadioGroup value={this.state.thread}>
              <Radio value="vision" onClick={ev => {
                this.state.client.publish(topics.SWITCH_CONTROLLER_EXEC, "vision")
              }}>Vision</Radio>
              <Radio value="controller" onClick={ev => {
                this.state.client.publish(topics.SWITCH_CONTROLLER_EXEC, "controller")
              }}>Controller</Radio>
            </RadioGroup>
          </DevSectionItem>
          <DevSectionItem>
            <DevSectionTitle>
              Locked
            </DevSectionTitle>
            <Switch
              checked={this.state.threadLocked}
              onClick={ev => {
                const topic = this.state.threadLocked
                  ? topics.RESUME_CONTROLLER
                  : topics.STOP_CONTROLLER

                this.state.client.publish(topic)
              }}
            />
          </DevSectionItem>
          <DevSectionItem>
            <DevSectionTitle>
              Pending
            </DevSectionTitle>
            <Switch
              checked={this.state.threadPending}
              disabled={!this.state.threadLocked}
              onClick={ev => {
                const topic = this.state.threadPending
                  ? topics.SWITCH_EXEC_NOT_PENDING
                  : topics.SWITCH_EXEC_PENDING

                this.state.client.publish(topic)
              }}
            />
          </DevSectionItem>
        </DevSection>
        <DevSection>
          <DevSectionTitle>Axis Movement</DevSectionTitle>
          <DevOption>
            <DevOptionTitle>MoveX</DevOptionTitle>
            <DevOptionInput onChange={ev => {
              this.setState({
                moveX: ev.target.value
              })
            }} placeholder="moveX" />
            <DevOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_MOVE_X, this.state.moveX)
            }}>Send Command</DevOptionButton>
          </DevOption>
          <DevOption>
            <DevOptionTitle>MoveY</DevOptionTitle>
            <DevOptionInput onChange={ev => {
              this.setState({
                moveY: ev.target.value
              })
            }} placeholder="moveY" />
            <DevOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_MOVE_Y, this.state.moveY)
            }}>Send Command</DevOptionButton>
          </DevOption>
          <DevOption>
            <DevOptionTitle>MoveZ</DevOptionTitle>
            <DevOptionInput onChange={ev => {
              this.setState({
                moveZ: ev.target.value
              })
            }} placeholder="moveZ"/>
            <DevOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_MOVE_Z, this.state.moveZ)
            }}>Send Command</DevOptionButton>
          </DevOption>
        </DevSection>
      </DevStyle>
    )
  }
}
