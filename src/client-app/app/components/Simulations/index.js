import React, {Component} from 'react'
import boxes from './boxes'
import SimulationRenderer from './SimulationRenderer'

export default class Simulations extends Component {
  render() {
    return (
      <SimulationRenderer boxes={boxes} />
    )
  }
}
