import {NavLink} from 'react-router-dom'
import styled from 'styled-components'
import {colors} from '../../styled/variables'

export const MenuContainer = styled.div`
  flex: 0 260px;
  width: 300px;
  border-right: 4px solid ${colors.grey["300"]};
`

export const MenuList = styled.ul`
  padding: 0;
  margin: 0;
  list-style: none;
`

export const MenuItem = styled(NavLink)`
  font-family: Calibre;
  font-weight: 800;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: block;
  padding: 24px 24px 24px 16px;
  margin: 12px;
  text-decoration: none;
  color: ${colors.grey["800"]};

  &:hover {
    background-color: ${colors.grey["100"]};
    border-radius: 2px;
  }

  &.active {

  }
`
