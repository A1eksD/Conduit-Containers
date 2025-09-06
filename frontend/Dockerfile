### ---------- 1. Build-Stage ----------
FROM node:20-alpine AS build

WORKDIR /src

COPY frontend/package*.json .

RUN npm ci

COPY frontend .

# erzeugt dist/
RUN npm run build


### ---------- 2. Runtime-Stage ----------
FROM nginx:1.27-alpine

WORKDIR /usr/share/nginx/html

COPY --from=build /src/dist .

EXPOSE 8282

CMD ["nginx", "-g", "daemon off;"]
