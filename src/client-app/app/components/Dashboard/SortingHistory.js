import React from 'react'
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'
import SimulationRenderer from '../Simulations/SimulationRenderer'
import {adaptBoxCoords} from '../../utils/simulation'

import * as actions from '../../actions'

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

const SortingHistory = ({vision, actions}) => {
  let history = []
  for(const id in vision.history) {
    const el = vision.history[id]
    let numOfBoxes = calculateRecursiveLength(el.boxes)
    if(numOfBoxes !== 0) {
      history.push({
        key: el.id,
        date: (new Date(el.dateCompleted)).toDateString(),
        boxes: calculateRecursiveLength(el.boxes),
        originalBoxes: el.boxes
      })
    }
  }

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
  }, {
    title: 'Opeartion',
    render: (text, record) => (
      <span>
        <a onClick={ev => {
          actions.processSendId(record.key)
          actions.processRequest()
        }}>Use pallet</a>
      </span>
    )
  }]

  return (
    <Section>
      <SectionTitle>Sorting History</SectionTitle>
      <Table
        dataSource={history}
        columns={columns}
        expandedRowRender={record => (
          <SimulationRenderer boxes={adaptBoxCoords(record.originalBoxes)} />
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

const mapDispatchToAction = dispatch => ({
  actions: bindActionCreators(actions, dispatch)
})

export default connect(mapStateToProps, mapDispatchToAction)(SortingHistory)
