import React, {Component} from 'react'
import mqtt from 'mqtt'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'
import * as actions from '../../actions'

import {Button, FloatingButtons} from '../../styled/components'
import {Section} from '../../styled/section'
import {MQTT_IP, topics} from '../../utils/config'
import SimulationRenderer from '../Simulations/SimulationRenderer'

class Dashboard extends Component {
  state = {
    client: mqtt.connect(MQTT_IP),
    processing: false,
    waiting: false,
    boxes: [],
    receivedBoxes: false,
    processingDone: false,
    img: ''
  }

  componentDidMount() {
    this.state.client.on('connect', () => {
      this.state.client.subscribe(topics.APP_RECEIVE_IMG)
      this.state.client.subscribe(topics.APP_RECEIVE_VISION_BOXES)
    })

    this.state.client.on('message',  (topic, msg) => {
      if(topic == topics.APP_RECEIVE_IMG && this.state.processing) {
        if(this.state.waiting) {
          this.setState({
            waiting: false,
            img: msg
          })
        }

        this.setState({
          img: msg
        })

        this.state.client.publish(topics.APP_REQUEST_IMG)
      }
      if(!this.state.processing) {
        console.log(1)
        this.setState({
          img: ''
        })
      }
      if(topic == topics.APP_RECEIVE_VISION_BOXES) {
        this.setState({
          boxes: JSON.parse(msg)
        })
      }
    })
  }

  componentWillUnmount() {
    if(this.state.processing) {
      // the user didn't press either button, so we must send
      // the controller a warning to stop the processing
      this.state.client.publish(topics.PROCESS_RESPONSE_CONTROLLER, "False")
    }

    const forceEnd = true
    this.state.client.end(forceEnd)
  }

  render() {
    let rendered

    if(this.state.processing && !this.state.waiting) {
      // should render a canvas with two buttons
      rendered = (
        <div>
          <img src={"data:image/jpeg;base64," + this.state.img} style={{float: 'left'}}/>
          <FloatingButtons>
            <Button onClick={ev => {
              this.state.client.publish(topics.PROCESS_RESPONSE_CONTROLLER, "True")
              this.setState({
                processing: false,
                img: '',
                processingDone: true,
              })
            }} type="primary">Accept Capture</Button>
            <Button onClick={ev => {
              this.state.client.publish(topics.PROCESS_RESPONSE_CONTROLLER, "False")
              this.setState({
                processing: false,
                img: ''
              })
            }} type="danger">Reject Capture</Button>
          </FloatingButtons>
        </div>
      )
    }
    else {
      rendered = (
        <div>
          <Section>
            <Button
              onClick={ev => {
                this.state.client.publish(topics.PROCESS_CONTROLLER)

                this.setState({
                  waiting: true,
                  processing: true,
                  processingDone: false
                }, () => {
                  this.setState({
                    boxes: []
                  })
                })
              }}
              disabled={this.state.waiting}
              loading={this.state.waiting}
              type="primary"
            >
              Start capturing
            </Button>
          </Section>
          {this.state.processingDone && this.state.boxes.length > 0 ? (
            <SimulationRenderer boxes={this.state.boxes} />
          ) : (
            null
          )}
        </div>
      )
    }

    return rendered
  }
}

const mapStateToProps = state => ({})

const mapDispatchToAction = dispatch => ({
  actions: bindActionCreators(actions, dispatch)
})

export default connect(mapStateToProps, mapDispatchToAction)(Dashboard)
