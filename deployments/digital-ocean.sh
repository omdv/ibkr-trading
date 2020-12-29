#!/bin/sh
curl -X POST -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer '$DOTOKEN'' -d \
    '{"name":"ibkr","region":"sfo2","size":"s-1vcpu-2gb","image":"docker-20-04"}' \
    "https://api.digitalocean.com/v2/droplets"