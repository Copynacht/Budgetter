FROM node:24-alpine

WORKDIR /app/budgetter-front

COPY ./budgetter-front/package*.json ./
RUN npm install

COPY ./budgetter-front .

RUN npm run generate

CMD cp -r .output/public/* /vol/www/nuxt
