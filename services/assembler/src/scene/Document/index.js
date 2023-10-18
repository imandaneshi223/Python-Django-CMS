import React from 'react';
import Helmet from 'react-helmet';
import {renderToString, renderToStaticMarkup} from "react-dom/server";
import assets from '../../../build/assets';
import { getDataFromTree } from "react-apollo"

const Document = ({ content, helmet, state }) => (
    <html {...(helmet.htmlAttributes.toComponent())}>
        <head>
            {helmet.title.toComponent()}
            {helmet.meta.toComponent()}
            {helmet.link.toComponent()}
            <link rel="stylesheet" href={assets.client.css} />
            <script src={assets.client.js} defer crossOrigin={process.env.NODE_ENV !== 'production' ? 'true' : 'false'}/>
            {helmet.script.toComponent()}
            {helmet.noscript.toComponent()}
        </head>
        <body {...(helmet.bodyAttributes.toComponent())}>
            <div id="root" dangerouslySetInnerHTML={{ __html: content }} />
        </body>
    </html>
);

export default (Content, context) => {
    return getDataFromTree(Content, context).then(
        () => {
            const content = renderToString(Content);
            const helmet = Helmet.renderStatic();
            const initialState = context.client.extract();
            const document = renderToStaticMarkup(<Document content={content} helmet={helmet} state={initialState} />);
            return  `<!DOCTYPE html>${document}`;
        }
    );

}
