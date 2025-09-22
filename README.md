# Conduit Containerized Application

## Project Overview
This repository bundles a **Django backend** and an **Angular frontend** that together implement the RealWorld / Conduit demo app. Both services are built via **multi-stage Dockerfiles** and orchestrated with **Docker Compose**.

> **Goal**  Spin-up the full stack with one command. Keep images tiny. Never ship secrets inside images.


## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Usage](#usage)
  - [Environment Variables](#environment-variables)
  - [Build Arguments](#build-arguments)
  - [Port Mapping](#port-mapping)
- [Architecture](#architecture)
  - [Multi‑Stage Builds](#multi-stage-builds)
  - [Runtime Diagram](#runtime-diagram)
- [Logging & Monitoring](#logging--monitoring)

---

## Repository Structure
```
.

├─ conduit-backend/         # Django project root
│     ├─ Dockerfile         # multi-stage backend build
│     ├─ container-entrypoint.sh
│     ├─ requirements.txt
│     ├─ .env.example  -> copy to .env
│     └─ …
├─ conduit-frontend/        # Angular project root
│     ├─ Dockerfile         # multi-stage frontend build
│     ├─ package.json
│     ├─ angular.json
│     ├─ .env.example  -> copy to .env
│     └─ …
├─ docker-compose.yaml      # orchestrates both services
├─ .gitignore               # ignores node_modules, __pycache__, secrets …
└─ README.md                # (this file)
```

---

## Prerequisites

- Docker
- Docker Compose

---

## Quickstart
1. **Clone repository**
```bash
git clone git@github.com:A1eksD/Conduit-Containers.git
cd conduit-containers
```
1. **Copy sample environment files and adjust if needed**
```bash
cp conduit-backend/example.env  conduit-backend/.env
```

1. **Build & run in detached mode**
```bash
docker-compose up --build -d
```
The first build can take a few minutes; subsequent builds are cached and faster.

> **Stop stack**
> ```bash
> docker compose down
> ```

---

## Usage
### Environment Variables
| Service  | Variable                     | Purpose                              |
|----------|------------------------------|--------------------------------------|
| Backend  | `DJANGO_SUPERUSER_USERNAME`  | Auto‑created admin user              |
|          | `DJANGO_SUPERUSER_PASSWORD`  | Admin password                       |
|          | `DJANGO_SUPERUSER_EMAIL`     | Admin mail                           |

Compose injects these files via `env_file:` — they **never** go into the final images.

### Build Arguments
| Arg            | Where        | Default | Notes |
|----------------|--------------|---------|-------|
| `BACKEND_PORT` | backend Dockerfile | 8383 | Used by `EXPOSE` and Gunicorn bind |
| `FRONTEND_PORT`| frontend Dockerfile | 8282 | Nginx listen port |

Override at build time:
```bash
docker compose build --build-arg BACKEND_PORT=8383 --build-arg FRONTEND_PORT=8282
```

### Port Mapping
Change only the **left** side of the `HOST:CONTAINER` pair inside `docker-compose.yaml`:
```yaml
ports:
  - "2222:8383"   # host 2222 → container 8383 (backend)
  - "1111:8282"   # host 1111 → container 8282 (frontend)
```

---

## Architecture

### Multi‑Stage Builds
1. **Builder stage**: installs compilers & dependencies, runs tests, produces artefacts.
2. **Runtime stage**: starts from a minimal base image and copies only the artefacts.

Benefits: image size ↓, attack surface ↓, build cache ↑.

### Runtime Diagram
```
┌────────────┐ 1111  ┌──────────────┐
│  nginx     │──────▶│  Gunicorn    │
│  Angular   │       │  Django API  │
└────────────┘       └──────────────┘
```

---

## Logging & Monitoring
**Stdout/Stderr** of each container → `docker logs <name>`
- Persist logs:
```bash
docker logs backend > backend-$(date +%F).log
docker logs frontend > frontend-$(date +%F).log
```
- Rotate logs automatically:
  ```yaml
  logging:
    driver: json-file
    options:
      max-size: "10m"
      max-file: "3"
  ```
Add this under a service in `docker-compose.yaml`.
