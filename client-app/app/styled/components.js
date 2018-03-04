import styled from 'styled-components'
import {Button as AntdButton} from 'antd'

export const AppStyle = styled.div`
  background-color: "#f0f0f0";
  height: 100%;
`

export const Content = styled.div`
  flex: 1 auto;
  padding: 16px;
`

export const Main = styled.div`
  display: flex;
  flex-flow: row wrap;
  height: 100%;

  & > * {
    flex: 1 auto;
  }
`

export const Button = styled(AntdButton)`
  margin: 12px 6px 0 0;
`
