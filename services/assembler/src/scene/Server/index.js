import {StaticRouter} from "react-router-dom";
import Application from "../Application";
import React from "react";
import { ApolloProvider } from "react-apollo";

export default (context, url) => (
    <ApolloProvider client={context.client}>
        <StaticRouter context={context} location={url}>
            <Application/>
        </StaticRouter>
    </ApolloProvider>
);