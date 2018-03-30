import React from 'react'
import {
  Section,
  SectionTitle
} from '../../styled/section'
import {
  ConnectionIcon
} from '../Menu/style'
import MdErrorOutline from 'react-icons/lib/md/error-outline'
import {NavLink} from 'react-router-dom'

const DisconnectedComponent = () => (
  <Section>
    <ConnectionIcon active={true}>
      <MdErrorOutline /> The controller is not connected.
      Go to <NavLink to="/settings">Settings</NavLink> to connect the system
    </ConnectionIcon>
  </Section>
)

export default DisconnectedComponent
