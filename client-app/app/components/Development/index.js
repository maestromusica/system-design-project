import React, {Component} from 'react'
import topics from '../../../../topics.json' // this is an ugly path...
import mqtt from 'mqtt'
import {
  Section,
  SectionItem,
  SectionTitle,
  SectionOption,
  SectionOptionInput,
  SectionOptionTitle,
  SectionOptionButton
} from '../../styled/section'
import {Button} from '../../styled/components'
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
      <div>
        <Section>
          <SectionItem>
            <SectionTitle>
              Thread
            </SectionTitle>
            <RadioGroup value={this.state.thread}>
              <Radio value="vision" onClick={ev => {
                this.state.client.publish(topics.SWITCH_CONTROLLER_EXEC, "vision")
              }}>Vision</Radio>
              <Radio value="controller" onClick={ev => {
                this.state.client.publish(topics.SWITCH_CONTROLLER_EXEC, "controller")
              }}>Controller</Radio>
            </RadioGroup>
          </SectionItem>
          <SectionItem>
            <SectionTitle>
              Locked
            </SectionTitle>
            <Switch
              checked={this.state.threadLocked}
              onClick={ev => {
                const topic = this.state.threadLocked
                  ? topics.RESUME_CONTROLLER
                  : topics.STOP_CONTROLLER

                this.state.client.publish(topic)
              }}
            />
          </SectionItem>
          <SectionItem>
            <SectionTitle>
              Pending
            </SectionTitle>
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
          </SectionItem>
        </Section>
        <Section>
          <SectionTitle>Axis Movement</SectionTitle>
          <SectionOption>
            <SectionOptionTitle>MoveX</SectionOptionTitle>
            <SectionOptionInput onChange={ev => {
              this.setState({
                moveX: ev.target.value
              })
            }} placeholder="moveX" />
            <SectionOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_MOVE_X, this.state.moveX)
            }}>Send Command</SectionOptionButton>
          </SectionOption>
          <SectionOption>
            <SectionOptionTitle>MoveY</SectionOptionTitle>
            <SectionOptionInput onChange={ev => {
              this.setState({
                moveY: ev.target.value
              })
            }} placeholder="moveY" />
            <SectionOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_MOVE_Y, this.state.moveY)
            }}>Send Command</SectionOptionButton>
          </SectionOption>
          <SectionOption>
            <SectionOptionTitle>MoveZ</SectionOptionTitle>
            <SectionOptionInput onChange={ev => {
              this.setState({
                moveZ: ev.target.value
              })
            }} placeholder="moveZ"/>
            <SectionOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_MOVE_Z, this.state.moveZ)
            }}>Send Command</SectionOptionButton>
          </SectionOption>
        </Section>
        <Section>
          <SectionTitle>Reset axis</SectionTitle>
          <SectionOption>
            <SectionOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_RESET_X)
              this.state.client.publish(topics.CONTROLLER_RESET_Y)
              this.state.client.publish(topics.CONTROLLER_RESET_Z)
            }} type="primary">
              Reset All
            </SectionOptionButton>
            <SectionOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_RESET_X)
            }}>
              Reset X
            </SectionOptionButton>
            <SectionOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_RESET_Y)
            }}>
              Reset Y
            </SectionOptionButton>
            <SectionOptionButton onClick={ev => {
              this.state.client.publish(topics.CONTROLLER_RESET_Z)
            }}>
              Reset Z
            </SectionOptionButton>
          </SectionOption>
        </Section>
        <Section>
          <SectionTitle>Actions</SectionTitle>
          {this.state.actions.length > 0 ? (
            <div>
              <Table
                dataSource={actions}
                columns={columns}
                size="small"
                bordered
              />
              {!this.state.threadPending ? (
                <Button onClick={ev => {
                  this.state.client.publish(topics.CONTROLLER_NEXT_ACTION)
                }}>Perform next action</Button>
              ) : (
                null
              )}
              <Button type="danger" onClick={ev => {
                this.state.client.publish(topics.CONTROLLER_DELETE, "all")
              }}>
                Delete all
              </Button>
            </div>
          ) : (
            <p>No actions in the thread</p>
          )}
        </Section>
      </div>
    )
  }
}
