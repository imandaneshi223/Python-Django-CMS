FROM node:10.10.0

ARG environment
ARG name

ENV SERVICE=$name
ENV ENVIRONMENT=$environment
ENV SOURCE=./services/$SERVICE
ENV DESTINATION=./dist

COPY $SOURCE/package*.json $DESTINATION/
WORKDIR $DESTINATION
RUN npm ci

COPY $SOURCE/public/ ./public
COPY $SOURCE/.env \
     $SOURCE/razzle.config.js \
     $SOURCE/docker-entrypoint.sh \
     ./
COPY $SOURCE/src/ ./src

RUN npm run build

EXPOSE 3000
ENTRYPOINT ["bash", "/dist/docker-entrypoint.sh"]