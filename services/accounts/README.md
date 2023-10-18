Authentication/authorization flow
--

* Anonymous user can `create` itself to receive `identity_token`
* Authenticated user provide aforementioned `identity_token` as request header
* Authenticated user can `update` his `accepted privacy policy` flag
* Authenticated user can provide data required for registration with `update`, to become registered user
* Registered user can provide password and username or email to receive `elevated_token`
* Logged in user provide aforementioned `elevated_token` as request header

Todo
-
* [x] Setup token authentication with login and registration
* [x] Setup ownership permissions
* [x] Setup selecting user by token, not only uuid
* [x] Setup services permissions 
* [x] Setup JWT authentication
* [ ] Hookup shared service authorization to accounts 
* [ ] Setup shared user authorization 
* [ ] Setup changing password 
* [ ] Choose and configure password hashing
* [ ] Gather user unique user-agent's
* [ ] Setup blocking user creation for bots
* [ ] Document accounts app endpoints 

Todo - Bugs
-
* [x] Admin interface is failing - "Unknown field(s) (user_service_permissions) specified for User. Check fields/fieldsets/exclude attributes of class AccountsUserAdmin."