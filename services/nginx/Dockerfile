FROM alpine:3.8 as builder

ARG environment
ARG host

ENV ENVIRONMENT=$environment
ENV HOST=$host

RUN apk update \
    && apk add findutils \
    && apk add sed

WORKDIR /build
ADD ./services/nginx/cert.$ENVIRONMENT/ ./cert
ADD ./services/nginx/nginx.conf ./nginx.conf
ADD ./services/nginx/conf.d.$ENVIRONMENT/ ./conf.d
RUN find /build/conf.d/* -type f -exec sed -i "s/<%HOST%>/$HOST/g" {} \;

FROM nginx:1.15.5-alpine

WORKDIR /etc/nginx/
RUN rm ./conf.d/default.conf && \
    rm ./nginx.conf
COPY --from=builder ./build/ .

