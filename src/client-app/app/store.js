import { createStore, applyMiddleware, combineReducers, compose } from 'redux'
import { routerMiddleware, routerReducer as routing, push } from 'react-router-redux'
import persistState from 'redux-localstorage'
import thunk from 'redux-thunk'
import logger from 'redux-logger'

import ips from './reducers/ips'
import {reduxMqttReducer, reduxMqttMiddleware} from './middlewares/redux-mqtt'
import * as actions from './actions'

export default function configureStore(initialState, routerHistory) {
  const router = routerMiddleware(routerHistory);

  const actionCreators = {
    ...actions,
    push
  };

  const reducers = {
    ips,
    routing,
    ...reduxMqttReducer
  };

  const middlewares = [ logger, thunk, router, reduxMqttMiddleware() ];

  const composeEnhancers = (() => {
    const compose_ = window && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__;
    if(process.env.NODE_ENV === 'development' && compose_) {
      return compose_({ actionCreators });
    }
    return compose;
  })();

  const enhancer = composeEnhancers(applyMiddleware(...middlewares), persistState());
  const rootReducer = combineReducers(reducers);

  return createStore(rootReducer, initialState, enhancer);
}
