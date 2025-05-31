FROM node:24-alpine

ARG NUXT_PUBLIC_API_BASE_URL

ENV NUXT_PUBLIC_API_BASE_URL=$NUXT_PUBLIC_API_BASE_URL

WORKDIR /app/budgetter-front

COPY ./budgetter-front/package*.json ./
RUN npm install

COPY ./budgetter-front .

RUN npm run generate

CMD cp -r .output/public/* /vol/www/nuxt
