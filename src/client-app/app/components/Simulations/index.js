import React, {Component} from 'react'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'

import boxes from './boxes'
import SimulationRenderer from './SimulationRenderer'
import {Button} from '../../styled/components'
import * as actions from '../../actions'

class Simulations extends Component {
  render() {
    return (
      <div>
        <SimulationRenderer boxes={boxes} />
        <Button onClick={ev => {
          this.props.actions.requestBoxes()
        }}>Request boxes</Button>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  meta: state.meta,
  thread: state.thread
})

const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators(actions, dispatch)
})

export default connect(mapStateToProps, mapDispatchToProps)(Simulations)
