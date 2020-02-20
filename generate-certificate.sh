#!/bin/bash

openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem \
    -subj "/C=HK/ST=Hong Kong/L=Hong Kong/O=Password Manager/OU=IT/CN=password manager"
