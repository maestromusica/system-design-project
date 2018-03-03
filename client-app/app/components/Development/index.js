import React, {Component} from 'react'
import topics from '../../../../topics.json' // this is an ugly path...
import mqtt from 'mqtt'
import {
  DevStyle,
  DevSection,
  DevSectionTitle,
  DevOption,
  DevOptionInput,
  DevOptionTitle,
  DevOptionButton} from './style'
import {Radio} from 'antd'
const RadioGroup = Radio.Group

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
      <DevStyle>
        <DevSection>
          <DevSectionTitle>
            Thread
          </DevSectionTitle>
          <RadioGroup onChange={ev => {
            console.log(ev.target.value)
          }} value={this.state.thread}>
            <Radio value="vision">Vision</Radio>
            <Radio value="controller">Controller</Radio>
          </RadioGroup>
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
