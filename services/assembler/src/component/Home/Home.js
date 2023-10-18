import React from 'react';
import logo from './react.svg';
import './Home.css';
import Helmet from 'react-helmet';
import User from '../User';

class Home extends React.Component {
    render() {
        return (
            <div className="Home">
                <Helmet>
                    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
                    <meta charSet="utf-8"/>
                    <title>Welcome to Razzle</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1"/>
                </Helmet>
                <div className="Home-header">
                    <img src={logo} className="Home-logo" alt="logo"/>
                    <h2>Welcome to Razzle over HTTPS DEV</h2>
                </div>
                <p className="Home-intro">
                    To get started, edit <code>src/App.js</code> or{' '}
                    <code>src/Home.js</code> and save to reload.
                </p>
                <User />
                <ul className="Home-resources">
                    <li>
                        <a href="https://github.com/jaredpalmer/razzle">Docs</a>
                    </li>
                    <li>
                        <a href="https://github.com/jaredpalmer/razzle/issues">Issues</a>
                    </li>
                    <li>
                        <a href="https://palmer.chat">Community Slack</a>
                    </li>
                </ul>
            </div>
        );
    }
}

export default Home;
