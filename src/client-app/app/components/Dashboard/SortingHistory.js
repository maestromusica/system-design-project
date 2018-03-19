import React from 'react'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'

import {
  Section,
  SectionTitle
} from '../../styled/section'

const SortingHistory = ({vision}) => {
  return (
    <Section>
      <SectionTitle>Sorting History</SectionTitle>
    </Section>
  )
}

const mapStateToProps = state => ({
  vision: state.vision
})

export default connect(mapStateToProps)(SortingHistory)
