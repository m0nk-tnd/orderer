FROM node:16-alpine as build
WORKDIR /app
COPY package.json /app/package.json
RUN printenv
RUN yarn install --only=prod
COPY . /app
RUN yarn build

FROM nginx:latest
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
