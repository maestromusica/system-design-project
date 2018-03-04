import React from 'react'
import topics from '../../../../topics.json' // this is an ugly path...
import {
  Section,
  SectionTitle,
  SectionOption,
  SectionOptionButton
} from '../../styled/section'

const ResetSection = ({client}) => (
  <Section>
    <SectionTitle>Reset axis</SectionTitle>
    <SectionOption>
      <SectionOptionButton onClick={ev => {
        client.publish(topics.CONTROLLER_RESET_X)
        client.publish(topics.CONTROLLER_RESET_Y)
        client.publish(topics.CONTROLLER_RESET_Z)
      }} type="primary">
        Reset All
      </SectionOptionButton>
      <SectionOptionButton onClick={ev => {
        client.publish(topics.CONTROLLER_RESET_X)
      }}>
        Reset X
      </SectionOptionButton>
      <SectionOptionButton onClick={ev => {
        client.publish(topics.CONTROLLER_RESET_Y)
      }}>
        Reset Y
      </SectionOptionButton>
      <SectionOptionButton onClick={ev => {
        client.publish(topics.CONTROLLER_RESET_Z)
      }}>
        Reset Z
      </SectionOptionButton>
    </SectionOption>
  </Section>
)

export default ResetSection
