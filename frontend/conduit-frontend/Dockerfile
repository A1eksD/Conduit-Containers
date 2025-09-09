### ---------- 1. Build-Stage ----------
FROM node:20-alpine AS build
WORKDIR /src

COPY package*.json .npmrc* ./   

RUN npm ci --no-audit --progress=false --legacy-peer-deps

COPY . .

RUN npm run build -- --configuration production


### ---------- 2. Runtime-Stage ----------
FROM nginx:1.27-alpine

WORKDIR /usr/share/nginx/html

COPY --from=build /src/dist/angular-conduit ./

EXPOSE 8282

CMD ["nginx", "-g", "daemon off;"]
