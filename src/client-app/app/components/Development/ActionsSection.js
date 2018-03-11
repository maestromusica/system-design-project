import React from 'react'
import {topics} from '../../utils/config'
import {
  Section,
  SectionTitle
} from '../../styled/section'
import {Button} from '../../styled/components'
import {Table} from 'antd'

const ActionsSection = ({meta, thread, actions}) => {
  let i = 0
  const actionsList = thread.actions.map((el) => {
    i += 1
    for(const topic in topics) {
      if(el.action == topics[topic]) {
        return {
          key: i,
          action: topic,
          payload: el.payload
        }
      }
    }
  })

  const columns = [{
    title: "#",
    dataIndex: "key",
    key: "key"
  }, {
    title: "Action",
    dataIndex: "action",
    key: "action"
  }, {
    title: "Payload",
    dataIndex: "payload",
    key: "payload"
  }, {
    title: "Operation",
    key: "delete",
    render: (text, record) => (
      <span>
        <a onClick={ev => {
          actions.deleteAction((record.key - 1).toString())
        }}>Delete</a>
      </span>
    )
  }]

  return (
    <Section>
      <SectionTitle>Actions</SectionTitle>
      {thread.actions.length > 0 ? (
        <div>
          <Table
            dataSource={actionsList}
            columns={columns}
            size="small"
            bordered
          />
          {!thread.pending ? (
            <Button onClick={ev => {
              acitons.requestNextAction()
            }}>Perform next action</Button>
          ) : (
            null
          )}
          <Button type="danger" onClick={ev => {
            actions.deleteAction('all')
          }}>
            Delete all
          </Button>
        </div>
      ) : (
        <p>No actions in the thread</p>
      )}
    </Section>
  )
}

export default ActionsSection
