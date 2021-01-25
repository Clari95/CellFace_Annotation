FROM node:12-alpine

EXPOSE 8080
WORKDIR /usr/src/app
COPY package.json yarn.lock ./
RUN yarn --no-progress