import {NavLink} from 'react-router-dom'
import styled from 'styled-components'
import {colors} from '../../styled/variables'
import LogoSvgSnort from './logo-snortx.svg'

export const MenuContainer = styled.div`
  flex: 0 220px;
  width: 300px;
  border-right: 4px solid ${colors.grey["300"]};
`

export const MenuList = styled.ul`
  padding: 0;
  margin: 0;
  list-style: none;
`

export const MenuItem = styled(NavLink)`
  font-family: 'Circular';
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 1px;
  display: block;
  padding: 10px 10px 10px 16px;
  margin: 6px;
  text-decoration: none;
  color: ${colors.grey["800"]};

  &:hover {
    background-color: ${colors.grey["100"]};
    border-radius: 2px;
  }

  &.active {

  }

  & svg {
    height: 24px;
    width: 24px;
    margin-right: 8px;
    margin-top: -4px;
    color: ${colors.grey["500"]};
    display: none;
  }
`
export const LogoSnort = styled(LogoSvgSnort)`
  height: 52px;
  display: block;
  margin-top: 40px;
  padding-left: 20px;
  margin-bottom: 20px;
`
