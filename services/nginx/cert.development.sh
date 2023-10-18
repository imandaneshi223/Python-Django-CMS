#!/usr/bin/env bash

source ../../.env

rm cert/*.crt
rm cert/*.key

openssl req \
    -x509 \
    -out cert.development/$HOST.crt \
    -keyout cert.development/$HOST.key \
    -newkey rsa:2048 -nodes -sha256 \
    -subj "/CN=$HOST" \
    -config "./cert/openssl.cnf" \
    -extensions v3_ca

certutil -d sql:$HOME/.pki/nssdb -A -t "P,," -n cert/$HOST.crt -i cert/$HOST.crt
certutil -d sql:$HOME/.pki/nssdb -L

find ./cert.development/*.cnf -type f -name 'xa*' -exec sed -i "s/<%HOST%>/$HOST/g" {} \;