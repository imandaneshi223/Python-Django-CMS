Development setup
--

- Not ready for anything more than a quick look
- Project uses symlinks to shared code
- Developed and tested only under Ubuntu 16.04 & 18.04

*Setup*

- rename all `.env.dist` files to `.env` 
- run `cert.development.sh` in nginx service to generate self signed certificate
- `docker-compose up`
- run migrations/add superusers in django containers

Goals
--
* [ ] Automatic import of new component types from JSON manifests
* [ ] Visual page builder allowing assembling sites/pages from pre-made react components
* [ ] Fast scaffolding of new services
* [ ] SSR out of the box 
* [ ] Full front-end tooling out of the box
* [ ] Integrated user tracking and analitycs
* [ ] Easy deployment and scaling 
* [ ] Easy to maintain and extend

Todo
--

* [ ] Rename project to `Enraged SOA`

*Services*
* [x] [Accounts service](https://github.com/gniewomir/django-react-cms/tree/master/services/accounts)
* [x] [GraphQL service](https://github.com/gniewomir/django-react-cms/tree/master/services/graphql)
* [x] [Web server](https://github.com/gniewomir/django-react-cms/tree/master/services/nginx)
* [ ] [Express+Razzle+React+Apollo](https://github.com/gniewomir/django-react-cms/tree/master/services/assembler)
* [ ] [Components/Routing service](https://github.com/gniewomir/django-react-cms/tree/master/services/cms)
* [ ] Setup shared component repository
* [ ] Setup Storybook service or [styleguidist?](https://github.com/styleguidist/react-styleguidist)
* [ ] Mailer service
* [ ] Media service
* [ ] Content service
* [ ] Search service
* [ ] Scrapper service  

*Maintenance/reliability/debugging*
* [ ] Sort out log levels to be based on env vars, log only to stdout
* [ ] Setup consistent logging format across project 
* [ ] Centralized logging 

*Security*
* [x] Setup SSL for development, to make dev and production environments as close as possible
* [x] Http only, secure cookies for fronted
* [X] JWT only for internal use 
* [ ] Setup services authentication & permissions on backend
* [ ] Non-root processes in containers
* [ ] Setup production configurations 
* [ ] Secure Django admin sites 

*Deployment*
* [x] Setup cleaner, properly cached, multi-stage Dockerfiles
* [ ] Automated build and pushing of images to Amazon ECR
* [ ] Automated deployment to Amazon ECS

Research 
--

* How to handle database migrations when deploying scaled containers without taking them all down? 
