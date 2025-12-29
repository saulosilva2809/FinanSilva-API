FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências de sistema (Pillow, psycopg2, etc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoints separados
COPY entrypoint.migrate.sh /entrypoint.migrate.sh
COPY entrypoint.no-migrate.sh /entrypoint.no-migrate.sh
RUN chmod +x /entrypoint.migrate.sh /entrypoint.no-migrate.sh

COPY src /app/src
