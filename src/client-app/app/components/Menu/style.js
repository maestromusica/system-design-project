import {NavLink} from 'react-router-dom'
import styled from 'styled-components'
import {colors} from '../../styled/variables'
import LogoSvgSnort from './logo-snortx.svg'

export const MenuContainer = styled.div`
  width: 240px;
  border-right: 1px solid ${colors.grey["300"]};
  background-color: ${colors.grey["50"]};
  height: 100vh;
  display: flex;
  flex-direction: column;
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
  color: ${colors.grey["900"]};

  &:hover {
    background-color: ${colors.grey["100"]};
    border-radius: 2px;
  }

  &.active {
    background-color: ${colors.grey["200"]}
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

export const ConnectionSection = styled.div`
  position: absolute;
  bottom: 16px;
  padding-left: 16px;
`

export const ConnectionIcon = styled.span`
  margin-right: 8px;

  & svg {
    height: 24px;
    width: 24px;
    color: ${props => props.active ? colors.grey['800'] : colors.grey['400']};
  }

  & span {
    margin-left: 6px;
  }
`
