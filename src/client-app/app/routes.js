import React from 'react';
import {Switch, Route, withRouter, BrowserRouter} from 'react-router';

import {AppStyle, Content, Main} from './styled/components'

import Menu from './components/Menu'
import Dashboard from './components/Dashboard'
import Development from './components/Development'
import Settings from './components/Settings'
import Simulations from './components/Simulations'
import withConnection from './hocs/withConnection'

const dev = withConnection(Development)
const sims = withConnection(Simulations)

const App = () => (
  <AppStyle>
    <Main>
      <Menu />
      <Content>
        <Switch>
          <Route exact path="/dashboard" component={Dashboard} />
          <Route exact path="/development" component={dev} />
          <Route exact path="/simulations" component={sims} />
          <Route exact path="/settings" component={Settings} />
        </Switch>
      </Content>
    </Main>
  </AppStyle>
)

export default App
