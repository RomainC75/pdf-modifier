FROM node:14-alpine

WORKDIR /server

COPY package*.json ./

RUN npm install

EXPOSE 3000

CMD ["npm", "start"]