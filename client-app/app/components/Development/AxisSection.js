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
    return (
      <Section>
        <SectionTitle>Axis Movement</SectionTitle>
        <SectionOption>
          <SectionOptionTitle>MoveX</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              moveX: ev.target.value
            })
          }} placeholder="moveX" />
          <SectionOptionButton onClick={ev => {
            this.props.client.publish(topics.CONTROLLER_MOVE_X, this.state.moveX)
          }}>
            Send Command
          </SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>MoveY</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              moveY: ev.target.value
            })
          }} placeholder="moveY" />
          <SectionOptionButton onClick={ev => {
            this.props.client.publish(topics.CONTROLLER_MOVE_Y, this.state.moveY)
          }}>
            Send Command
          </SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>MoveZ</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              moveZ: ev.target.value
            })
          }} placeholder="moveZ"/>
          <SectionOptionButton onClick={ev => {
            this.props.client.publish(topics.CONTROLLER_MOVE_Z, this.state.moveZ)
          }}>
            Send Command
          </SectionOptionButton>
        </SectionOption>
      </Section>
    )
  }
}
