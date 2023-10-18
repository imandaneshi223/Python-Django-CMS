import Server from '../../scene/Server';
import document from '../../scene/Document';

export const createRendererMiddleware = () => {
    return async (req, res, next) => {
        const context = {
            client: res.locals.client
        };
        try {
            const response = await document(Server(context, req.url), context);
            res.status(200);
            res.send(response);
            res.end()
        } catch (error) {
            console.log(error);
            res.status(500);
            res.send('Internal server error!');
            res.end()
        }
        next()

    }
};
