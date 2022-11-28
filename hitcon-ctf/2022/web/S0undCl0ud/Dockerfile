FROM docker:dind

COPY instancer /www
COPY service /service
WORKDIR /www

RUN apk add --no-cache --update nodejs npm
RUN npm install

RUN chmod +x /www/docker-entrypoint.sh
