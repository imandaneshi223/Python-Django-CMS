module.exports = {
    secret: process.env.SECRET_KEY,
    services: {
        accounts:   process.env.SERVICE_URL_ACCOUNTS,
        assembler:  process.env.SERVICE_URL_ASSEMBLER,
        components: process.env.SERVICE_URL_COMPONENTS,
        redis:      process.env.SERVICE_URL_REDIS,
        graphql:    process.env.SERVICE_URL_GRAPHQL
    }
};
