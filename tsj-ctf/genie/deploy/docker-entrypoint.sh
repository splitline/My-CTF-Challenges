#!/bin/sh

rm -f /var/run/docker.pid
dockerd &
sleep 3s

if [ "$(docker images -q service:latest 2> /dev/null)" == "" ]; then
    docker build -t service:latest ./service
fi

/usr/bin/node ./server.js
