import { createStore, applyMiddleware, combineReducers, compose } from 'redux';
import { routerMiddleware, routerReducer as routing, push } from 'react-router-redux';
import persistState from 'redux-localstorage';
import thunk from 'redux-thunk';

import ips from './reducers/ips';
import {reduxMqttReducer, reduxMqttMiddleware} from './middlewares/redux-mqtt'
import ipActions from './actions/ips';
import {MQTT_IP} from './utils/config'

export default function configureStore(initialState, routerHistory) {
  const router = routerMiddleware(routerHistory);

  const actionCreators = {
    ...ipActions,
    push
  };

  const reducers = {
    ips,
    routing,
    ...reduxMqttReducer
  };

  const middlewares = [ thunk, router, reduxMqttMiddleware(MQTT_IP) ];

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
