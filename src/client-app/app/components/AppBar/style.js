import styled from 'styled-components'
import {colors} from '../../styled/variables'
import LogoSvg from './logo-sortx.svg'

export const Header = styled.header`
  height: 60px;
  border-bottom: 4px solid ${colors.grey["300"]}
`
export const Logo = styled(LogoSvg)`
  height: 52px;
  display: block;
  margin-top: 40px;
  padding-left: 20px;
  margin-bottom: 20px
`
