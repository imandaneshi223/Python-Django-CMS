const {ApolloServer} = require('apollo-server');
const types = require('./src/types');
const resolvers = require('./src/resolvers');
const sources = require('./src/sources');
const context = require('./src/context');

const server = new ApolloServer({
    typeDefs: types,
    resolvers: resolvers,
    dataSources: sources,
    context: context,
});

server.listen().then(({url}) => {
    console.log(`🚀  Server ready at ${url}`);
});