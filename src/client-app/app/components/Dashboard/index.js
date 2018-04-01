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
import withConnection from '../../hocs/withConnection'

class Dashboard extends Component {

  _sendRequestImg = (props) => {
    if(props.vision.processing && !props.vision.processingDone) {
      this.props.actions.requestImg()
    }
  }

  componentDidMount() {
    this._sendRequestImg(this.props)
  }

  componentWillUpdate(nextProps) {
    this._sendRequestImg(nextProps)
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

    const ConnectedControls = withConnection(() => <Controls
      vision={this.props.vision}
      thread={this.props.thread}
      actions={this.props.actions} />
    )

    return (
      <div>
        <ConnectedControls />
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
          <SimulationRenderer boxes={this.props.vision.boxes} />
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
