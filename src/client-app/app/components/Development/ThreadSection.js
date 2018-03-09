import React from 'react'
import topics from '../../../../config/topics.json' // this is an ugly path...
import {
  Section,
  SectionItem,
  SectionTitle
} from '../../styled/section'
import {Radio, Switch} from 'antd'
const RadioGroup = Radio.Group

const ThreadSection = ({client, thread, threadPending, threadLocked}) => (
  <Section>
    <SectionItem>
      <SectionTitle>
        Thread
      </SectionTitle>
      <RadioGroup value={thread}>
        <Radio value="vision" onClick={ev => {
          client.publish(topics.SWITCH_CONTROLLER_EXEC, "vision")
        }}>Vision</Radio>
        <Radio value="controller" onClick={ev => {
          client.publish(topics.SWITCH_CONTROLLER_EXEC, "controller")
        }}>Controller</Radio>
      </RadioGroup>
    </SectionItem>
    <SectionItem>
      <SectionTitle>
        Locked
      </SectionTitle>
      <Switch
        checked={threadLocked}
        onClick={ev => {
          const topic = threadLocked
            ? topics.RESUME_CONTROLLER
            : topics.STOP_CONTROLLER

          client.publish(topic)
        }}
      />
    </SectionItem>
    <SectionItem>
      <SectionTitle>
        Pending
      </SectionTitle>
      <Switch
        checked={threadPending}
        disabled={!threadLocked}
        onClick={ev => {
          const topic = threadPending
            ? topics.SWITCH_EXEC_NOT_PENDING
            : topics.SWITCH_EXEC_PENDING

          client.publish(topic)
        }}
      />
    </SectionItem>
  </Section>
)

export default ThreadSection
