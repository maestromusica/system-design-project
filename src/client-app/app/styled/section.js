import styled from 'styled-components'
import {colors} from './variables'
import {Button, Input} from 'antd'

export const Section = styled.div`
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid ${colors.grey["300"]};

  &::after, &::before {
    display: table;
    content: ' ';
    clear: both;
  }
`

export const SectionItem = styled.div`
  float: left;
  padding-right: 16px;
  margin-right: 16px;
  ${'' /* border-right: 1px solid ${colors.grey["300"]}; */}
`

export const SectionTitle = styled.h3`
  font-family: Calibre;
  font-weight: 800;
  font-size: 14px;
  padding: 0;
  margin: 0;
  text-transform: uppercase;
  margin-bottom: 12px;
`

export const SectionOption = styled.div`
  display: flex;
  flex-flow: row;
  flex: 1 auto;
  align-items: center;
  margin-bottom: 10px;
`

export const SectionOptionTitle = styled.h4`
  margin-right: 8px;
`

export const SectionOptionButton = styled(Button)`
  margin: 0 4px;
`

export const SectionOptionInput = styled(Input).attrs({
})`
  width: 200px;
`
