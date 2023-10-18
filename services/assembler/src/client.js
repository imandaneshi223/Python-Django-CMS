import React from 'react';
import {hydrate} from 'react-dom';
import Client from './scene/Client';

hydrate(
    <Client/>,
    document.getElementById('root')
);

if (module.hot) {
    module.hot.accept();
}
