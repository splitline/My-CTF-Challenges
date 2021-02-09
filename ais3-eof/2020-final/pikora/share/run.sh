#! /bin/sh
rm /var/run/docker.pid
dockerd &
sleep 5s
docker pull python:3.9-alpine
ncat -vc 'timeout 500 python3 /ctf/main.py' -kl 0.0.0.0 48763