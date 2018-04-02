import React, {Component} from 'react';
import {Switch, Route, withRouter} from 'react-router';
import styled, {keyframes} from 'styled-components'
import LogoSvg from './components/AppBar/logo-sortx.svg'

import {AppStyle, Content, Main} from './styled/components'

import Menu from './components/Menu'
import Dashboard from './components/Dashboard'
import Development from './components/Development'
import Settings from './components/Settings'
import Simulations from './components/Simulations'
import withConnection from './hocs/withConnection'
import Transition from 'react-transition-group/Transition';

const enterAnimation = keyframes`
  0% {opacity: 0}
  100% {opacity: 1}
`

const leaveAnimation = keyframes`
  0% {opacity: 0}
  40% {opacity: 1}
  60% {opacity: 1}
  100% {opacity: 0}
`

const Logo = styled(LogoSvg)`
  height: 60px;
  display: block;
  margin-right: auto;
  margin-left: auto;
  align-self: center;
  animation-name: ${leaveAnimation};
  animation-duration: 1s;
`

const Animated = styled(Main)`
  animation-name: ${enterAnimation};
  animation-duration: 0.4s;
`

const dev = withConnection(Development)
const sims = withConnection(Simulations)

class App extends Component {
  state = {
    renderedLogo: true,
    shouldRender: false
  }

  componentDidMount() {
    this.props.history.push("/development")
    setTimeout(() => {
      this.setState({
        renderedLogo: false
      }, () => {
        this.setState({
          shouldRender: true
        })
      })
    }, 900)
  }

  render() {
    let displayFlex = {}
    if(!this.state.shouldRender) {
      displayFlex = {
        display: 'flex'
      }
    }
    return (
      <AppStyle style={displayFlex}>
        {this.state.shouldRender ? (
          <Animated>
            <Menu />
            <Content>
              <Switch>
                <Route exact path="/development" default component={Dashboard} />
                <Route path="/development" component={dev} />
                <Route path="/simulations" component={sims} />
                <Route path="/settings" component={Settings} />
              </Switch>
            </Content>
          </Animated>
        ) : (
          <Logo />
        )}
      </AppStyle>
    )
  }
}

export default withRouter(App)
