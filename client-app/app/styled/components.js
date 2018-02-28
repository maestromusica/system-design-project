import styled from 'styled-components'

export const AppStyle = styled.div`
  background-color: "#f0f0f0";
  height: 100%;
  width: 100%;
`

export const Content = styled.div`
  flex: 1 auto;
`

export const Main = styled.div`
  display: flex;
  flex-flow: row wrap;
  height: 100%;

  & > * {
    flex: 1 auto;
  }
`
