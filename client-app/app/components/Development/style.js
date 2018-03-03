import styled from 'styled-components'
import {Button, Input} from 'antd'
import {colors} from '../../styled/variables'

export const DevStyle = styled.div`

`

export const DevSection = styled.div`
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid ${colors.grey["300"]}
`

export const DevSectionTitle = styled.h3`
  font-family: Calibre;
  font-weight: 800;
  font-size: 14px;
  padding: 0;
  margin: 0;
  text-transform: uppercase;
  margin-bottom: 12px;
`

export const DevOption = styled.div`
  display: flex;
  flex-flow: row;
  flex: 1 auto;
  align-items: center;
  margin-bottom: 10px;
`

export const DevOptionTitle = styled.h4`
  margin-right: 8px;
`

export const DevOptionButton = styled(Button)`
  margin: 0 4px;
`

export const DevOptionInput = styled(Input).attrs({
})`
  width: 200px;
`
