import React, {Component} from 'react'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'

import boxes from './boxes'
import SimulationRenderer from './SimulationRenderer'
import {Button} from '../../styled/components'
import * as actions from '../../actions'

class Simulations extends Component {
  state = {
    waiting: false,
    boxes: boxes
  }

  componentWillReceiveProps(nextProps) {
    if(
      this.props.simulation.boxesRequested
      && !nextProps.simulation.boxesRequested
      && this.state.waiting
    ) {
      // this means we requested boxes and now we received them!
      this.setState({
        waiting: false,
        boxes: nextProps.simulation.boxes
      })
      console.log(nextProps.simulation.boxes)
    }
  }

  render() {
    return (
      <div>
        <SimulationRenderer boxes={this.state.boxes} />
        <Button onClick={ev => {
          this.props.actions.requestBoxes()
          this.setState({
            waiting: true
          })
        }} loading={this.state.waiting}>Request boxes</Button>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  meta: state.meta,
  thread: state.thread,
  simulation: state.simulation
})

const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators(actions, dispatch)
})

export default connect(mapStateToProps, mapDispatchToProps)(Simulations)
