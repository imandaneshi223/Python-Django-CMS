module.exports = {
    modify: (config, {target, dev}, webpack) => {
        /**
         * Required until next release of Razzle, where explicitly setting CLIENT_PUBLIC_PATH should be enough
         */
        if (target === 'web' && dev) {
            config.output.publicPath = process.env.CLIENT_PUBLIC_PATH;
        }
        if (target === 'node' && dev) {
            config.output.publicPath = process.env.CLIENT_PUBLIC_PATH;
        }
        return config;
    },
};