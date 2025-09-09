### ---------- 1. Build-Stage ----------
FROM python:3.10-alpine AS builder

WORKDIR /build

COPY requirements.txt .

# → Wheels separat erzeugen
RUN apk add --no-cache gcc musl-dev \
    && pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt


### ---------- 2. Runtime-Stage ----------
FROM python:3.10-alpine

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY . /app

# → nur echte Wheels installieren
RUN pip install --no-cache-dir /wheels/*.whl \
    && chmod +x /app/container-entrypoint.sh \
    && rm -rf /wheels

EXPOSE 8383

ENTRYPOINT ["/app/container-entrypoint.sh"]
