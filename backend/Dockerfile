### ---------- 1. Build-Stage ----------
FROM python:3.10-alpine AS builder

WORKDIR /build

COPY backend/requirements.txt .

RUN apk add --no-cache gcc musl-dev \
 && pip wheel --no-cache-dir --no-deps -r requirements.txt


### ---------- 2. Runtime-Stage ----------
FROM python:3.10-alpine

WORKDIR /app
# nur Wheels + Code kopieren - Wheels* (.whl) sind vorkompilierte Python-Pakete.
COPY --from=builder /build /wheels

COPY backend /app

RUN pip install --no-cache /wheels/* \
 && chmod +x /app/container-entrypoint.sh

ENV PYTHONUNBUFFERED=1

EXPOSE 8383

ENTRYPOINT ["/app/container-entrypoint.sh"]
