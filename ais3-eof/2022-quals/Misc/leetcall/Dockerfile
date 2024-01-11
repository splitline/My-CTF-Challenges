FROM docker:dind

RUN apk add --update --no-cache python3 py-pip nmap-ncat

RUN pip install epicbox rich

WORKDIR /ctf
ENTRYPOINT "/ctf/run.sh"
