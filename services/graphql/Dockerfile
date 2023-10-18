FROM node:10.10.0 as builder

ARG environment
ARG name

ENV SERVICE=$name
ENV ENVIRONMENT=$environment
ENV SOURCE=./services/$SERVICE

COPY $SOURCE/package*.json /build/
WORKDIR /build
RUN npm ci
COPY $SOURCE/src/ ./src
COPY $SOURCE/.env \
     $SOURCE/docker-entrypoint.sh \
     $SOURCE/index.js \
     ./

FROM node:10.10.0

ENV DESTINATION=./dist

WORKDIR $DESTINATION
COPY --from=builder ./build/ .
ENTRYPOINT ["bash", "/dist/docker-entrypoint.sh"]