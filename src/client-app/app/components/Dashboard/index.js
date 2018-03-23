import React, {Component} from 'react'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'
import * as actions from '../../actions'

import {Button, FloatingButtons} from '../../styled/components'
import {Section} from '../../styled/section'
import {MQTT_IP, topics} from '../../utils/config'
import SimulationRenderer from '../Simulations/SimulationRenderer'
import SortingHistory from './SortingHistory'
import Controls from './Controls'

const boxes = [[
  {
    height: 6,
    width: 9,
    depth: 18,
    x: 0,
    y: 0,
    z: 0,
    color: 'yellow'
  }, {
    height: 6,
    width: 12,
    depth: 12,
    x: 9,
    y: 0,
    z: 0,
    color: 'blue'
  }, {
    height: 6,
    width: 9,
    depth: 9,
    x: 21,
    y: 0,
    z: 0,
    color: 'purple'
  }
]]

class Dashboard extends Component {

  componentWillUpdate(nextProps) {
    console.log(2)
    if(nextProps.vision.processing && !nextProps.vision.processingDone) {
      console.log(1)
      this.props.actions.requestImg()
    }
  }

  componentWillUnmount() {
    // if(this.state.processing) {
    //   // the user didn't press either button, so we must send
    //   // the controller a warning to stop the processing
    //   this.state.client.publish(topics.PROCESS_RESPONSE_CONTROLLER, "False")
    // }
    //
    // const forceEnd = true
    // this.state.client.end(forceEnd)
  }

  render() {
    let rendered
    const state = this.props.vision
    const actions = this.props.actions

    if(state.processing && !state.waiting) {
      // should render a canvas with two buttons
      rendered = (
        <div>
          <img
            src={"data:image/jpeg;base64," + state.img}
            style={{float: 'left'}}
          />
          <FloatingButtons>
            <Button onClick={ev => {
              actions.processResponse("True")
            }} type="primary">Accept Capture</Button>
            <Button onClick={ev => {
              actions.processResponse("False")
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
                actions.processRequest()
              }}
              disabled={state.waiting}
              loading={state.waiting}
              type="primary"
            >
              Start capturing
            </Button>
          </Section>
          {state.processingDone && state.boxes.length > 0 ? (
            <SimulationRenderer boxes={state.boxes} />
          ) : (
            null
          )}
        </div>
      )
    }

    return (
      <div>
        <Controls
          vision={this.props.vision}
          thread={this.props.thread}
          actions={this.props.actions}
        />
        {this.props.vision.processing && !this.props.vision.waiting ? (
          <Section>
            <img
              src={"data:image/jpeg;base64," + state.img}
              style={{float: 'left'}}
            />
            <FloatingButtons>
              <Button onClick={ev => {
                actions.processResponse("True")
              }} type="primary">Accept Capture</Button>
              <Button onClick={ev => {
                actions.processResponse("False")
              }} type="danger">Reject Capture</Button>
            </FloatingButtons>
          </Section>
        ) : (
          null
        )}
        {this.props.vision.processingDone && this.props.vision.sorting ? (
          <SimulationRenderer boxes={boxes} />
        ) : (
          null
        )}
        <SortingHistory />
      </div>
    )
  }
}

const mapStateToProps = state => ({
  vision: state.vision,
  thread: state.thread
})

const mapDispatchToAction = dispatch => ({
  actions: bindActionCreators(actions, dispatch)
})

export default connect(mapStateToProps, mapDispatchToAction)(Dashboard)
