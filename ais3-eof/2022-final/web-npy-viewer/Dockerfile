FROM node:latest

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./app .

COPY ./flag /fl4444g

RUN npm install

# auto kill container after 10 minutes
CMD [ "timeout", "600", "node", "app.js" ]
