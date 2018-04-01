import React from 'react'
import {connect} from 'react-redux'

import DisconnectedComponent from '../components/DisconnectedComponent'

const withConnection = (Component) => {
  const mapStateToProps = (state) => ({
    meta: state.meta
  })

  const func = ({meta}) => {
    if(meta.connected) {

      if(typeof(Component) == "function") {
        return <Component />
      }
      else if(typeof(Component) == "object") {
        return <Component />
      }
    }
    else {
      return <DisconnectedComponent />
    }
  }

  return connect(mapStateToProps)(func)
}

const mapStateToProps = (state) => ({
  meta: state.meta
})

export default withConnection
