### ---------- 1. Build-Stage ----------
FROM node:20-alpine AS build
WORKDIR /src

COPY . $WORKDIR

RUN npm install

RUN npm run build

### ---------- 2. Runtime-Stage ----------
FROM nginx:1.27-alpine

WORKDIR /usr/share/nginx/html

COPY --from=build /src/dist/angular-conduit ./

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
