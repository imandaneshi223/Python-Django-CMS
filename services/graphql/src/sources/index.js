const AccountsService = require('./accounts.js');
const sources = () => {
    return {
        AccountsService: new AccountsService()
    };
};
module.exports = sources;
