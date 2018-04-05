import React, {Component} from 'react'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'

import boxes from './boxes'
import SimulationRenderer from './SimulationRenderer'
import {adaptBoxCoords} from '../../utils/simulation'

import {Button} from '../../styled/components'
import * as actions from '../../actions'
import {
  Section,
  SectionTitle,
  SectionOption,
  SectionOptionInput,
  SectionOptionButton
} from '../../styled/section'

class Simulations extends Component {
  state = {
    waiting: false,
    boxes: boxes,
    palletId: ""
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
    }
  }

  render() {
    return (
      <div>
        <SimulationRenderer boxes={adaptBoxCoords(this.state.boxes)} />
        <Section>
          <SectionTitle>
            Request boxes
          </SectionTitle>
          <SectionTitle></SectionTitle>
          <SectionOption>
            <SectionOptionInput
              onChange={ev => {
                this.setState({
                  palletId: ev.target.value
                })
              }}
              placeholder="Pallet ID"
              value={this.state.palletId}
            />
            <SectionOptionButton onClick={ev => {
              this.props.actions.requestBoxes(this.state.palletId)
              this.setState({
                waiting: true
              })
            }} loading={this.state.waiting}>Request boxes</SectionOptionButton>
          </SectionOption>
        </Section>
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
