import React, {Component} from 'react'
import mqtt from 'mqtt'
import {Button} from '../../styled/components'
import topics from '../../../../topics.json' // this is an ugly path...

const LOCALHOST_IP = "mqtt://127.0.0.1"

export default class Dashboard extends Component {
  state = {
    client: mqtt.connect(LOCALHOST_IP),
    processing: false,
    waiting: false,
    img: ''
  }

  componentDidMount() {
    this.state.client.on('connect', () => {
      this.state.client.subscribe(topics.APP_RECIEVE_IMG)
    })

    this.state.client.on('message',  (topic, msg) => {
      console.log(topic, msg)
      if(topic == topics.APP_RECIEVE_IMG) {
        if(this.state.waiting) {
          this.setState({
            waiting: false,
            img: msg
          })
        }

        this.setState({
          img: msg
        })
        for(let i=0; i<10; i++) {
          this.state.client.publish(topics.APP_REQUEST_IMG)
        }
      }
      if(!this.state.processing) {
        this.setState({
          img: ''
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
          <img src={"data:image/jpeg;base64," + this.state.img} />
          <Button onClick={ev => {
            this.state.client.publish(topics.PROCESS_RESPONSE_CONTROLLER, "True")
            this.setState({
              processing: false,
              img: ''
            })
          }} type="primary">Accept Capture</Button>
          <Button onClick={ev => {
            this.state.client.publish(topics.PROCESS_RESPONSE_CONTROLLER, "False")
            this.setState({
              processing: false,
              img: ''
            })
          }} type="danger">Reject Capture</Button>
        </div>
      )
    }
    else {
      rendered = (
        <Button onClick={ev => {
          this.state.client.publish(topics.PROCESS_CONTROLLER)
          this.setState({
            waiting: true,
            processing: true
          })
        }}>Start capturing</Button>
      )
    }

    if(this.state.waiting) {
      rendered = (<p>Waiting for video feed</p>)
    }

    return rendered
  }
}
