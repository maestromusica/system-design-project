import styled from 'styled-components'
import {
  Button as AntdButton,
  Radio as AntdRadio
} from 'antd'
const AntdRadioGroup = AntdRadio.Group

export const AppStyle = styled.div`
  background-color: "#f0f0f0";
  height: 100%;
`

export const Content = styled.div`
  flex: 1 auto;
  padding: 16px;
  padding-top: 60px;
  padding-left: 40px;
  overflow: auto;
`

export const Main = styled.div`
  display: flex;
  flex-flow: row wrap;
  height: 100%;
`

export const Button = styled(AntdButton)`
  margin: 12px 6px 0 0;
`

export const RadioGroup = styled(AntdRadioGroup)`
  display: block;
  margin-top: 24px;
`

export const RadioAligned = styled(AntdRadio)`
  display: block;
  margin-bottom: 8px;
`

export const FloatingButtons = styled.div`
  float: left;
  margin-left: 16px;

  & button {
    display: block;
  }
`
