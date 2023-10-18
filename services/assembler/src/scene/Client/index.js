import Application from '../Application';
import BrowserRouter from 'react-router-dom/BrowserRouter';
import React from 'react';
import {ApolloProvider} from "react-apollo";
import {ApolloClient} from 'apollo-client';
import {createHttpLink} from 'apollo-link-http';
import {InMemoryCache} from 'apollo-cache-inmemory';

const link = createHttpLink({
    uri: 'https://enraged.local/graphql',
    credentials: 'same-origin'
});

const client = new ApolloClient({
    cache: new InMemoryCache(),
    link,
});

export default () => (
    <ApolloProvider client={client}>
        <BrowserRouter>
            <Application/>
        </BrowserRouter>
    </ApolloProvider>
);