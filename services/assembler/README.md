AUTHENTICATION/AUTHORIZATION
--

*Rules*
* this service do not recognize or accept JWT tokens
* authorization header takes precedence over authorization cookie, 
  but can be used only to updated authorization cookie
* cookies are http only, java script should not have access to it to prevent XSS attacks
* cookies are secure and are transferred only over encrypted connection, 
  to prevent hijacking identity_token or elevated_token 
* tokens should not be used to identify user for analytics purposes, 
  for analytics purposes there will be introduced special kind of token analytics_token

*Flow*
* Every user automatically receives cookie with his identity_token if he doesnt have one,
  this happens with any request that hits authorization middleware
* If registered user wants to log in, he have to obtain elevated_token by performing login mutation,
  and perform `/update-auth-cookie` request authorized with elevated_token in header to update cookie
* If logged in user wants to log out, he have to obtain identity_token back by performing logout mutation
  and perform `/update-auth-cookie` request with identity_token in authorization header to update cookie

TODO
--

* [ ] Setup /login and /register endpoints to remove ugly `/update-cookie` hack 
* [ ] Hookup routing based on components service list of routes 
* [ ] Secure Express with [Helmet](https://github.com/helmetjs/helmet)
* [ ] Sign cookies - so hijacked/leaked token wont be enough to perform action on behalf of user   
* [ ] Introduce analytics_token which identifies user, but cannot be used to authenticate/authorize user
 
