import fetch from 'node-fetch';
import gql from 'graphql-tag';
import {ApolloClient} from 'apollo-client';
import {createHttpLink} from 'apollo-link-http';
import {InMemoryCache} from 'apollo-cache-inmemory';

const createGraphQLClient = (token) => {
    return new ApolloClient({
        ssrMode: true,
        link: createHttpLink({
            uri: process.env.SERVICE_URL_GRAPHQL,
            credentials: 'same-origin',
            headers: token ? {
                authorization: token
            } : {},
            fetch
        }),
        cache: new InMemoryCache(),
    });
};

const setAuthorizationCookie = (res, token) => {
    res.cookie('authorization', token, {
        httpOnly: true,
        secure: true,
        maxAge: 60 * 60 * 24 * 365 * 20 * 1000, // 20 years
        domain: process.env.HOST
    });
};

const authenticateUser = (res, token) => {
    if (!token || token.substring(0, 5) !== 'Token') {
        throw new Error('No token!');
    }
    return createGraphQLClient(token);
};


const authenticateNewUser = async (res) => {
    const user = await createGraphQLClient().query({
        query: gql`
            query {
              userIdentity {
                token
              }
            }
        `,
    });
    setAuthorizationCookie(res, `Token ${user.data.userIdentity.token}` );
    return createGraphQLClient(`Token ${user.data.userIdentity.token}`);
};

export const createUpdateAuthCookieMiddleware = () => {
    return (req, res, next) => {
        try {
            if (!req.header('authorization') || req.header('authorization').substring(0, 5) !== 'Token') {
                console.error(`User provided invalid token. Cannot update cookie.`);
                res.status(401).end();
                return;
            }
            setAuthorizationCookie(res, req.header('authorization'));
            res.status(200).end()
        } catch (error) {
            console.error(error);
            res.status(401).end()
        }
    };
};

export const createAuthorizationMiddleware = () => {
    return async (req, res, next) => {
        try {
            res.locals.client = await authenticateUser(res, req.cookies.authorization);
        } catch (error) {
            console.log('Creating new user.');
            res.locals.client = await authenticateNewUser(res);
        }
        if (!res.locals.client) {
            console.error('GraphQL client not created!');
            res.status(401).send('Authentication error!');
            return;
        }
        next();
    }
};

