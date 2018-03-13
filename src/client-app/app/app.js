import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import {applyMiddleware} from 'redux'
import {ConnectedRouter} from 'react-router-redux';
import {createMemoryHistory} from 'history';
import App from './routes';
import configureStore from './store';

const syncHistoryWithStore = (store, history) => {
  const { routing } = store.getState();
  if(routing && routing.location) {
    history.replace(routing.location);
  }
};

const initialState = {};
const routerHistory = createMemoryHistory();
let store = configureStore(initialState, routerHistory);
syncHistoryWithStore(store, routerHistory);

// const rootElement = document.querySelector(document.currentScript.getAttribute('data-container'));
const rootElement = document.getElementById('app');

ReactDOM.render(
  <Provider store={store}>
    <ConnectedRouter history={routerHistory}>
      <App />
    </ConnectedRouter>
  </Provider>,
  rootElement
);
