import React, {Component} from 'react'
import {MenuContainer, MenuList, MenuItem} from './style'
import {NavLink} from 'react-router-dom'
import {Logo} from '../AppBar/style'
import {LogoSnort} from './style'
import Connections from './Connections'

import MdCode from 'react-icons/lib/md/code'
import MdSettings from 'react-icons/lib/md/settings'
import MdDashboard from 'react-icons/lib/md/dashboard'
import MdDonutSmall from 'react-icons/lib/md/donut-small'

export default class Menu extends Component {
  state = {
    useSnort: false
  }

  render() {
    return (
      <MenuContainer>
        <div onClick={ev => {
          this.setState({
              useSnort: !this.state.useSnort
          })
        }}>
          {this.state.useSnort ? (
            <LogoSnort />
          ) : (
            <Logo />
          )}
        </div>
        <MenuList>
          <MenuItem to="/">
            <MdDashboard />
            Dashboard
          </MenuItem>
          <MenuItem to="/simulations">
            <MdDonutSmall />
            Simulations
          </MenuItem>
          <MenuItem to="/development">
            <MdCode />
            Development
          </MenuItem>
          <MenuItem to="/settings">
            <MdSettings />
            Settings
          </MenuItem>
        </MenuList>
        <Connections />
      </MenuContainer>
    )
  }
}
