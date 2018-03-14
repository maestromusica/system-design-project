import React, {Component} from 'react'
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
    moveZ: undefined,
    moveGrabber: undefined,
    moveRotate: undefined
  }

  _sendMoveX = () => {
    this.props.actions.moveX(this.state.moveX)
    this.setState({
      moveX: undefined
    })
  }

  _sendMoveY = () => {
    this.props.actions.moveY(this.state.moveY)
    this.setState({
      moveY: undefined
    })
  }

  _sendMoveZ = () => {
    this.props.actions.moveZ(this.state.moveZ)
    this.setState({
      moveZ: undefined
    })
  }

  _sendMoveGrabber = () => {
    this.props.actions.grab(this.state.moveGrabber)
    this.setState({
      moveGrabber: undefined
    })
  }

  _sendMoveRotate = () => {
    this.props.actions.rotate(this.state.moveRotate)
    this.setState({
      moveRotate: undefined
    })
  }

  render() {
    const disabledX = !this.state.moveX
    const disabledY = !this.state.moveY
    const disabledZ = !this.state.moveZ
    const disabledGrabber = !this.state.moveGrabber
    const disabledRotate = !this.state.moveRotate

    return (
      <Section>
        <SectionTitle>Axis Movement</SectionTitle>
        <SectionOption>
          <SectionOptionTitle>MoveX</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              moveX: ev.target.value
            })
          }} placeholder="moveX" value={this.state.moveX} onKeyPress={ev => {
            if(ev.key == 'Enter') {
              this._sendMoveX()
            }
          }} />
          <SectionOptionButton
            onClick={ev => this._sendMoveX()}
            disabled={disabledX}
          >
            Send Command
          </SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>MoveY</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              moveY: ev.target.value
            })
          }} placeholder="moveY" value={this.state.moveY} onKeyPress={ev => {
            if(ev.key == 'Enter') {
              this._sendMoveY()
            }
          }}/>
          <SectionOptionButton onClick={ev => this._sendMoveY()} disabled={disabledY}>
            Send Command
          </SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>MoveZ</SectionOptionTitle>
          <SectionOptionInput
            onChange={ev => {
              this.setState({
                moveZ: ev.target.value
              })
            }}
            placeholder="moveZ"
            value={this.state.moveZ}
            onKeyPress={ev => {
              if(ev.key == 'Enter') {
                this._sendMoveZ()
              }
            }}
          />
          <SectionOptionButton
            onClick={ev => this._sendMoveZ()}
            disabled={disabledZ}>
            Send Command
          </SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>Move grabber</SectionOptionTitle>
          <SectionOptionInput
            onChange={ev => {
              this.setState({
                moveGrabber: ev.target.value
              })
            }}
            placeholder="move grabber"
            value={this.state.moveGrabber}
            onKeyPress={ev => {
              if(ev.key == 'Enter') {
                this._sendMoveGrabber()
              }
            }}
          />
          <SectionOptionButton
            onClick={ev => this._sendMoveGrabber()}
            disabled={disabledGrabber}
          >
            Send Command
          </SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>Rotate grabber</SectionOptionTitle>
          <SectionOptionInput
            onChange={ev => {
              this.setState({
                moveRotate: ev.target.value
              })
            }}
            placeholder="rotate grabber"
            value={this.state.moveRotate}
            onKeyPress={ev => {
              if(ev.key == 'Enter') {
                this._sendMoveRotate()
              }
            }}
          />
          <SectionOptionButton
            onClick={ev => this._sendMoveRotate()}
            disabled={disabledRotate}
          >
            Send command
          </SectionOptionButton>
        </SectionOption>
      </Section>
    )
  }
}
