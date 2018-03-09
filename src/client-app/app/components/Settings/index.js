import React, {Component} from 'react'
import {
  Section,
  SectionTitle,
  SectionOption,
  SectionOptionTitle,
  SectionOptionInput,
  SectionOptionButton
} from '../../styled/section'

export default class Settings extends Component {
  render() {
    return (
      <div>
        <Section>
          <SectionTitle>IP Settings</SectionTitle>
          <SectionOption>
            <SectionOptionTitle>Controller IP</SectionOptionTitle>
            <SectionOptionInput />
            <SectionOptionButton onClick={ev => {
              
            }}>Save IP</SectionOptionButton>
          </SectionOption>
          <SectionOption>
            <SectionOptionTitle>EV3 INF_11</SectionOptionTitle>
            <SectionOptionInput />
            <SectionOptionButton>Save IP</SectionOptionButton>
          </SectionOption>
          <SectionOption>
            <SectionOptionTitle>EV3 INF_31</SectionOptionTitle>
            <SectionOptionInput />
            <SectionOptionButton>Save IP</SectionOptionButton>
          </SectionOption>
        </Section>
      </div>
    )
  }
}
