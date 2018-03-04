import React, {Component} from 'react'
import topics from '../../../../topics.json' // this is an ugly path...
import {
  Section,
  SectionTitle,
  SectionOption,
  SectionOptionInput,
  SectionOptionTitle,
  SectionOptionButton
} from '../../styled/section'

export default class AxisSection extends Component {
  state = {
    moveX: undefined,
    moveY: undefined,
    moveZ: undefined
  }

  render() {
    const disabledX = !this.state.moveX
    const disabledY = !this.state.moveY
    const disabledZ = !this.state.moveZ
    return (
      <Section>
        <SectionTitle>Axis Movement</SectionTitle>
        <SectionOption>
          <SectionOptionTitle>MoveX</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              moveX: ev.target.value
            })
          }} placeholder="moveX" value={this.state.moveX} />
          <SectionOptionButton onClick={ev => {
            this.props.client.publish(topics.CONTROLLER_MOVE_X, this.state.moveX)
            this.setState({
              moveX: undefined
            })
          }} disabled={disabledX}>
            Send Command
          </SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>MoveY</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              moveY: ev.target.value
            })
          }} placeholder="moveY" value={this.state.moveY} />
          <SectionOptionButton onClick={ev => {
            this.props.client.publish(topics.CONTROLLER_MOVE_Y, this.state.moveY)
            this.setState({
              moveY: undefined
            })
          }} disabled={disabledY}>
            Send Command
          </SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>MoveZ</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              moveZ: ev.target.value
            })
          }} placeholder="moveZ" value={this.state.moveZ} />
          <SectionOptionButton onClick={ev => {
            this.props.client.publish(topics.CONTROLLER_MOVE_Z, this.state.moveZ)
            this.setState({
              moveZ: undefined
            })
          }} disabled={disabledZ}>
            Send Command
          </SectionOptionButton>
        </SectionOption>
      </Section>
    )
  }
}
