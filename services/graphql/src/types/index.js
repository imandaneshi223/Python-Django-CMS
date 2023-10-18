const { gql } = require('apollo-server');

types = gql` 

    type UserIdentity {
        token: String!
    }
    
    type UserBackendIdentity {
        jwt_token: String!
    }
    
    type UserInfo {
        token: String!
        is_loggedin: Boolean
        is_registered: Boolean
        accepted_privacy_policy: Boolean
        accepted_terms_of_service: Boolean   
        email: String
        first_name: String
        last_name: String 
    }
    
    type User  {
        identity_token: String!
        elevated_token: String
        is_registered: Boolean
        accepted_privacy_policy: Boolean
        accepted_terms_of_service: Boolean
        username: String
        email: String
        first_name: String
        last_name: String
    }
    
    input ExchangeTokenInput {
        token: String!
    }
    
    type Query {
        userIdentity: UserIdentity
        exchangeToken(input: ExchangeTokenInput): UserBackendIdentity
        userInfo: UserInfo
        user: User
    }
    
    input AcceptPrivacyPolicy {
        accepted_privacy_policy: Boolean!
    }
    
    input CollectEmailInput {
        email: String!
    }
            
    input RegisterUserInput {
        email: String!
        password: String!
        accepted_privacy_policy: Boolean!
        accepted_terms_of_service: Boolean!
        first_name: String
        last_name: String
    }

    input LoginUserInput {
        email: String!
        password: String!
    }
    
    input UpdateUserInput {
        email: String
        first_name: String
        last_name: String
        accepted_privacy_policy: Boolean
        accepted_terms_of_service: Boolean
    }
    
    type Mutation {
        acceptPrivacyPolicy(input: AcceptPrivacyPolicy): UserInfo
        collectEmail(input: CollectEmailInput): UserInfo
        registerUser(input: RegisterUserInput): UserInfo
        loginUser(input: LoginUserInput): UserInfo
        logoutUser: UserIdentity
        updateUser(input: UpdateUserInput): UserInfo        
    }
`;

module.exports = types;