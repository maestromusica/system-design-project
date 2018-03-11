import React from 'react'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'

import ThreadSection from './ThreadSection'
import AxisSection from './AxisSection'
import ResetSection from './ResetSection'
import ActionsSection from './ActionsSection'

import * as actions from '../../actions'

const Development = ({meta, thread, actions}) => (
  <div>
    <ThreadSection
      actions={actions}
      thread={thread}
      meta={meta}
    />
    <AxisSection
      actions={actions}
    />
    <ResetSection
      actions={actions}
    />
    <ActionsSection
      actions={actions}
      meta={meta}
      thread={thread}
    />
  </div>
)

const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators(actions, dispatch)
})

const mapStateToProps = state => ({
  meta: state.meta,
  thread: state.thread
})

export default connect(mapStateToProps, mapDispatchToProps)(Development)
