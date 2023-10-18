import React from 'react';
import Route from 'react-router-dom/Route';
import Switch from 'react-router-dom/Switch';
import Home from '../../component/Home/Home';

export default () => (
    <Switch>
        <Route exact path="/" component={Home}/>
    </Switch>
);