import React from 'react'
import {MenuContainer, MenuList, MenuItem} from './style'
import {NavLink} from 'react-router-dom'

const Menu = () => (
  <MenuContainer>
    <MenuList>
      <MenuItem to="/">Dashboard</MenuItem>
      <MenuItem to="/development">Development</MenuItem>
      <MenuItem to="/settings">Settings</MenuItem>
    </MenuList>
  </MenuContainer>
)

export default Menu
