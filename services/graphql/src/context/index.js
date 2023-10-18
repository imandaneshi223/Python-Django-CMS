const {services: {accounts}, secret} = require('../config');
const fetch = require('node-fetch');
const {verify} = require('jsonwebtoken');
const {to} = require('await-to-js');
const {AuthenticationError} = require('apollo-server');

const createUser = async () => {
    const [response_error, response] = await to(fetch(`${accounts}/user/`, {method: 'post'}));
    if (response_error) {
        return {
            error: response_error
        }
    }
    const [decoding_error, json] = await to(response.json());
    if (decoding_error) {
        return {
            error: decoding_error
        }
    }
    return {
        created: true,
        user: json,
        token: json.identity_token,
        jwt_auth: `Bearer ${json.jwt_token}`,
        auth: `Token ${json.identity_token}`,
        auth_method: `token`
    };
};

const getUser = async (token) => {
    const [response_error, response] = await to(fetch(
        `${accounts}/user/${token}`,
        {
            method: 'get',
            headers: {
                'authorization': `Token ${token}`
            }
        }
    ));
    if (response_error) {
        return {
            error: response_error
        }
    }
    const [decoding_error, json] = await to(response.json());
    if (decoding_error) {
        return {
            error: decoding_error
        }
    }
    return {
        user: json,
        token: token,
        jwt_auth: `Bearer ${json.jwt_token}`,
        auth: `Token ${token}`,
        auth_method: `token`
    };
};

const checkUserToken = (token) => {
    let user = {};
    try {
        user = verify(token, secret);
    } catch (error) {
        return {
            error
        }
    }
    return {
        user,
        token,
        jwt_auth: `Bearer ${token}`,
        auth: `Bearer ${token}`,
        auth_method: `jwt`
    }
};

const rejectOrResolve = (context) => {
    return context.error
        ? Promise.reject(typeof context.error === 'string' ? new AuthenticationError(context.error) : context.error)
        : Promise.resolve(context);
};

module.exports = ({req}) => {
    if (!req.headers.authorization) {
        return rejectOrResolve(createUser());
    }
    const [type, token] = req.headers.authorization.split(' ');
    if (token && type === 'Token') {
        return rejectOrResolve(getUser(token));
    }
    if (token && type === 'Bearer') {
        return rejectOrResolve(checkUserToken(token));
    }
    return Promise.reject(new AuthenticationError('Invalid authentication header!'));
};