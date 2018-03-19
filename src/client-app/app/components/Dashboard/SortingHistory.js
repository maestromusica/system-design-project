import React from 'react'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'
import SimulationRenderer from '../Simulations/SimulationRenderer'

import {
  Section,
  SectionTitle
} from '../../styled/section'
import {Table} from 'antd'

const calculateRecursiveLength = arr => {
  let length = 0
  arr.forEach(el => {
    length += el.length
  })

  return length
}

const SortingHistory = ({vision}) => {
  const history = vision.history.map((el, key) => {
    return {
      key: key + 1,
      date: (new Date(el.dateCompleted)).toDateString(),
      boxes: calculateRecursiveLength(el.boxes),
      originalBoxes: el.boxes
    }
  })

  const columns = [{
    title: "#",
    dataIndex: "key",
    key: "key"
  }, {
    title: "Date completed",
    dataIndex: "date",
    key: "date"
  }, {
    title: "# of boxes",
    dataIndex: "boxes",
    key: "boxes"
  }]

  return (
    <Section>
      <SectionTitle>Sorting History</SectionTitle>
      <Table
        dataSource={history}
        columns={columns}
        expandedRowRender={record => (
          <SimulationRenderer boxes={record.originalBoxes} />
        )}
        size="small"
        bordered
      />
    </Section>
  )
}

const mapStateToProps = state => ({
  vision: state.vision
})

export default connect(mapStateToProps)(SortingHistory)
