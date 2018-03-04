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
import {Radio, Switch, Table} from 'antd'
const RadioGroup = Radio.Group

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
    let i = 0
    const actions = this.state.actions.map((el) => {
      i += 1
      for(const topic in topics) {
        if(el.action == topics[topic]) {
          return {
            key: i,
            action: topic,
            payload: el.payload
          }
        }
      }
    })
    const columns = [{
      title: "#",
      dataIndex: "key",
      key: "key"
    }, {
      title: "Action",
      dataIndex: "action",
      key: "action"
    }, {
      title: "Payload",
      dataIndex: "payload",
      key: "payload"
    }, {
      title: "Operation",
      key: "delete",
      render: (text, record) => (
        <span>
          <a onClick={ev => {
            this.state.client.publish(topics.CONTROLLER_DELETE, (record.key - 1).toString())
          }}>Delete</a>
        </span>
      )
    }]

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
        <DevSection>
          <DevSectionTitle>Reset axis</DevSectionTitle>
          <DevOption>
            <DevOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_RESET_X)
              this.state.client.publish(topics.CONTROLLER_RESET_Y)
              this.state.client.publish(topics.CONTROLLER_RESET_Z)
            }} type="primary">
              Reset All
            </DevOptionButton>
            <DevOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_RESET_X)
            }}>
              Reset X
            </DevOptionButton>
            <DevOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_RESET_Y)
            }}>
              Reset Y
            </DevOptionButton>
            <DevOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_RESET_Z)
            }}>
              Reset Z
            </DevOptionButton>
          </DevOption>
        </DevSection>
        <DevSection>
          <DevSectionTitle>Actions</DevSectionTitle>
          {this.state.actions.length > 0 ? (
            <div>
              <Table
                dataSource={actions}
                columns={columns}
                size="small"
                bordered
              />
              <DevOptionButton type="danger" onClick={ev => {
                this.state.client.publish(topics.CONTROLLER_DELETE, "all")
              }}>
                Delete all
              </DevOptionButton>
            </div>
          ) : (
            <p>No actions in the thread</p>
          )}
        </DevSection>
      </DevStyle>
    )
  }
}
