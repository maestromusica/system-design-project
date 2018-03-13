import React from 'react'
import {connect} from 'react-redux'
import {
  ConnectionSection,
  ConnectionIcon
} from './style'

import MdBluetooth from 'react-icons/lib/md/bluetooth'
import MdBluetoothDisabled from 'react-icons/lib/md/bluetooth-disabled'
import MdCast from 'react-icons/lib/md/cast'
import MdCastConnected from 'react-icons/lib/md/cast-connected'

const Connections = ({meta}) => (
  <ConnectionSection>
    <ConnectionIcon active={meta.connected}>
      {meta.connected ? (
        <MdBluetooth />
      ) : (
        <MdBluetoothDisabled />
      )}
    </ConnectionIcon>
    <ConnectionIcon active={meta.connected && meta.ev3Connected}>
      {meta.ev3Connected && meta.connected ? (
        <MdCastConnected />
      ) : (
        <MdCast />
      )}
    </ConnectionIcon>
  </ConnectionSection>
)

const mapStateToProps = state => ({
  meta: state.meta
})

export default connect(mapStateToProps)(Connections)
