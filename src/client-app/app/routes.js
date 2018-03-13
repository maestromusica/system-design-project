import React from 'react';
import {Switch, Route, withRouter, BrowserRouter} from 'react-router';

import {AppStyle, Content, Main} from './styled/components'

import Menu from './components/Menu'
import Dashboard from './components/Dashboard'
import Development from './components/Development'
import Settings from './components/Settings'
import Simulations from './components/Simulations'

const App = () => (
  <AppStyle>
    <Main>
      <Menu />
      <Content>
        <Switch>
          <Route exact path="/" component={Dashboard} />
          <Route exact path="/development" component={Development} />
          <Route exact path="/settings" component={Settings} />
          <Route exact path="/simulations" component={Simulations} />
        </Switch>
      </Content>
    </Main>
  </AppStyle>
)

export default App
