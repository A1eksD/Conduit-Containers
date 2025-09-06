# Conduit Containerized Application

## Project Overview
The repository contains a **Django backend** and a **React (Vite) frontend** that together implement the Conduit demo application. Both services are packaged as lightweight Docker images via **multi‑stage builds** and orchestrated with **Docker Compose**.

> Goal: spin‑up the full stack with one command, keep images small, and avoid shipping secrets.


## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Usage](#usage)
  - [Environment Variables](#environment-variables)
  - [Build Arguments](#build-arguments)
  - [Customizing Ports](#customizing-ports)
- [Architecture](#architecture)
  - [Multi‑Stage Builds](#multi-stage-builds)
  - [Runtime Diagram](#runtime-diagram)
- [Logging & Monitoring](#logging--monitoring)

---

## Repository Structure
```
.
├─ backend/              # Django project
│  ├─ Dockerfile         # multi‑stage backend image
│  ├─ requirements.txt   # Python deps
│  ├─ container-entrypoint.sh
│  └─ .env.example
├─ frontend/             # React UI
│  ├─ Dockerfile         # multi‑stage frontend image
│  ├─ package.json
│  └─ .env.example
├─ docker-compose.yaml   # orchestrates both services
├─ .gitignore            # excludes node_modules, __pycache__, etc.
└─ README.md             # you are here
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
cd conduit
```
1. **Copy sample environment files and adjust if needed**
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

1. **Build & run in detached mode**
```bash
$ docker compose up --build -d
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
| Frontend | `VITE_API_URL`               | Base URL of backend API              |

Create real `.env` files **outside** the images; Compose injects them at container start (see `env_file:` directives).

### Build Arguments
| Arg            | Where        | Default | Notes |
|----------------|--------------|---------|-------|
| `BACKEND_PORT` | backend/Dockerfile | 8383 | Used by `EXPOSE` and Gunicorn bind |
| `FRONTEND_PORT`| frontend/Dockerfile | 8282 | Nginx listen port |

Override at build time:
```bash
docker compose build --build-arg BACKEND_PORT=9000
```

### Customizing Ports
Host ↔ container port mappings live in `ports:`; change the **left** side only:
```yaml
ports:
  - "5000:8383"  # host 5000 → container 8383
```

---

## Architecture
![architecture](docs/architecture.svg)

### Multi‑Stage Builds
1. **Builder stage**: installs compilers & dependencies, runs tests, produces artefacts.
2. **Runtime stage**: starts from a minimal base image and copies only the artefacts.

Benefits: image size ↓, attack surface ↓, build cache ↑.

### Runtime Diagram
```
┌───────────┐    HTTP     ┌────────────┐
│  nginx    │────────────▶│  backend   │
│  (8282)   │            │  gunicorn  │
└───────────┘            └────────────┘
       ▲                        │
       └──────── static files ◀─┘
```

---

## Logging & Monitoring
- **Stdout/Stderr** of each container is captured by Docker. View with:
  ```bash
  docker logs backend_1
  docker logs frontend_1
  ```
- Export logs to a file:
  ```bash
  docker logs backend_1 > backend-$(date +%F).log
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
