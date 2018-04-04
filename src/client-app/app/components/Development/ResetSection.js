import React from 'react'
import {
  Section,
  SectionTitle,
  SectionOption,
  SectionOptionButton
} from '../../styled/section'

const ResetSection = ({actions}) => (
  <Section>
    <SectionTitle>Reset axis</SectionTitle>
    <SectionOption>
      <SectionOptionButton onClick={ev => {
        actions.resetX()
        actions.resetY()
        action.resetZ()
      }} type="primary">
        Reset All
      </SectionOptionButton>
      <SectionOptionButton onClick={ev => {
        actions.resetX()
      }}>
        Reset X
      </SectionOptionButton>
      <SectionOptionButton onClick={ev => {
        actions.resetY()
      }}>
        Reset Y
      </SectionOptionButton>
      {/* <SectionOptionButton onClick={ev => {
        actions.resetZ()
        }}>
        Reset Z
      </SectionOptionButton> */}
    </SectionOption>
  </Section>
)

export default ResetSection
