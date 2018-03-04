import React, {Component} from 'react'
import mqtt from 'mqtt'
import {Button} from 'antd'
import topics from '../../../../topics.json' // this is an ugly path...

const LOCALHOST_IP = "mqtt://127.0.0.1"

class VideoFeed extends Component {
  componentDidMount() {
    const ctx = this.refs.canvas.getContext('2d')
    this.updateVideoFeed()
  }

  componentWillReceiveProps(nextProps) {
    this.updateVideoFeed(nextProps)
  }

  updateVideoFeed(data) {
    const ctx = this.refs.canvas.getContext('2d')
    const arr = data ? data : this.props.data
    console.log(1)
    console.log(1, arr)
    const uint8Arr = new Uint8ClampedArray(arr)
    const imageData = new ImageData(uint8Arr, 720, 1280)

    ctx.putImageData(imageData, 0, 0)
  }

  render() {
    return (
      <canvas
        ref="canvas"
        width={this.props.width}
        height={this.props.height}
      ></canvas>
    )
  }
}

export default class Dashboard extends Component {
  state = {
    client: mqtt.connect(LOCALHOST_IP),
    processing: false,
    waiting: false
  }

  componentDidMount() {
    this.state.client.on('connect', () => {
      this.state.client.subscribe(topics.APP_RECIEVE_IMG)
    })

    this.state.client.on('message',  (topic, msg) => {
      if(topic == topics.APP_RECIEVE_IMG) {
        if(this.state.waiting) {
          this.setState({
            waiting: false,
            img: msg
          })
        }
        console.log(msg)
        this.setState({
          img: msg
        })
      }
    })
  }

  render() {
    let rendered

    if(this.state.processing && !this.state.waiting) {
      // should render a canvas with two buttons
      rendered = (
        <div>
          {/* <VideoFeed height="1000" width="700" data={this.state.img} /> */}
          <img src={"data:image/jpeg;base64," + this.state.img} />
          <Button onClick={ev => {
            this.state.client.publish(topics.PROCESS_RESPONSE_CONTROLLER, "False")
            this.setState({
              processing: false
            })
          }}>End processing</Button>
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
