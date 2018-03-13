import React, {Component} from 'react'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'
import * as actions from '../../actions'

import {
  Section,
  SectionTitle,
  SectionOption,
  SectionOptionTitle,
  SectionOptionInput,
  SectionOptionButton
} from '../../styled/section'
import {
  Button
} from '../../styled/components'

class Settings extends Component {
  state = {
    CLIENT: this.props.ips.CLIENT,
    INF_11: this.props.ips.INF_11,
    INF_31: this.props.ips.INF_31
  }

  render() {
    return (
      <Section>
        <SectionTitle>IP Settings</SectionTitle>
        <SectionOption>
          <SectionOptionTitle>Client IP</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              CLIENT: ev.target.value
            })
          }} value={this.state.CLIENT} />
          <SectionOptionButton onClick={ev => {
            this.props.actions.addControllerIP(this.state.CLIENT)
          }}>Save IP</SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>EV3 INF_11</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              INF_11: ev.target.value
            })
          }} value={this.state.INF_11} />
          <SectionOptionButton onClick={ev => {
            this.props.actions.add11IP(this.state.INF_11)
          }}>Save IP</SectionOptionButton>
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>EV3 INF_31</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.setState({
              INF_31: ev.target.value
            })
          }} value={this.state.INF_31} />
          <SectionOptionButton onClick={ev => {
            this.props.actions.add31IP(this.state.INF_31)
          }}>
            Save IP
          </SectionOptionButton>
        </SectionOption>
        <Button type="primary" onClick={ev => {
          this.props.actions.restartClient()
        }}>Connect</Button>
      </Section>
    )
  }
}

const mapStateToProps = state => ({
  ips: state.ips,
  meta: state.meta
})

const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators(actions, dispatch)
})

export default connect(mapStateToProps, mapDispatchToProps)(Settings)
