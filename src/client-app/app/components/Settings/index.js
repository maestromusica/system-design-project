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
            this.props.actions.addControllerIP(ev.target.value)
          }} value={this.props.ips.CLIENT} />
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>EV3 INF_11</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.props.actions.add11IP(ev.target.value)
          }} value={this.props.ips.INF_11} />
        </SectionOption>
        <SectionOption>
          <SectionOptionTitle>EV3 INF_31</SectionOptionTitle>
          <SectionOptionInput onChange={ev => {
            this.props.actions.add31IP(ev.target.value)
          }} value={this.props.ips.INF_31} />
        </SectionOption>
        <Button type="primary" onClick={ev => {
          this.props.actions.restartClient()
        }}>Connect controller</Button>
        <Button onClick={ev => {
          this.props.actions.connectEV3()
        }}>
          Connect EV3
        </Button>
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
