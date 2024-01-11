#!/bin/sh

rm -f /var/run/docker.pid
dockerd &
sleep 3s

if [ "$(docker images -q service:latest 2> /dev/null)" == "" ]; then
    echo "[debug] docker build -t service:latest --build-arg AUTO_DESTROY=$AUTO_DESTROY /service"
    docker build -t service:latest --build-arg AUTO_DESTROY=$AUTO_DESTROY /service
fi

NODE_ENV=production /usr/bin/node app.js
