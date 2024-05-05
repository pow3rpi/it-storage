FROM node:18-alpine

WORKDIR /react-app

COPY . .

RUN npm ci --omit-dev --no-audit

ENTRYPOINT npm start
