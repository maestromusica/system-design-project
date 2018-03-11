import React from 'react'
import {
  Section,
  SectionItem,
  SectionTitle
} from '../../styled/section'
import {Radio, Switch} from 'antd'
const RadioGroup = Radio.Group

const VISION_TAG = "vision"
const CONTROLLER_TAG = "controller"

const ThreadSection = ({meta, thread, actions}) => (
  <Section>
    <SectionItem>
      <SectionTitle>
        Thread
      </SectionTitle>
      <RadioGroup value={thread.name}>
        <Radio value="vision" onClick={ev => {
          actions.switchExecutionThread(VISION_TAG)
        }}>Vision</Radio>
        <Radio value="controller" onClick={ev => {
          actions.switchExecutionThread(CONTROLLER_TAG)
        }}>Controller</Radio>
      </RadioGroup>
    </SectionItem>
    <SectionItem>
      <SectionTitle>
        Locked
      </SectionTitle>
      <Switch
        checked={thread.locked}
        onClick={ev => {
          if(thread.locked) {
            actions.resumeController()
          }
          else {
            actions.stopController()
          }
        }}
      />
    </SectionItem>
    <SectionItem>
      <SectionTitle>
        Pending
      </SectionTitle>
      <Switch
        checked={thread.pending}
        disabled={!thread.locked}
        onClick={ev => {
          if(thread.pending) {
            actions.switchExecToNotPending()
          }
          else {
            actions.switchExecToPending()
          }
        }}
      />
    </SectionItem>
  </Section>
)

export default ThreadSection
