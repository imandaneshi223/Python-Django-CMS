import gql from "graphql-tag";
import {Query} from "react-apollo";
import React from 'react';

export default () => (
    <Query query={gql`
                    query {
                      user {
                            identity_token
                            elevated_token
                            is_registered
                            accepted_privacy_policy
                            accepted_terms_of_service
                            username
                            email
                            first_name
                            last_name
                      }
                    }
           `}
           pollInterval={500000}
    >
        {({loading, error, data}) => {
            if (loading) return null;
            if (error) return `Error! ${error.message}`;
            return (
                <pre>
                    {JSON.stringify(data)}
                </pre>
            );
        }}
    </Query>
);