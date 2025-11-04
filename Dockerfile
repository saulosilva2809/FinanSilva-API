FROM python:3.12-slim

# Evita criação de .pyc e habilita logs não bufferizados
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências básicas para build de pacotes Python que exigem compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências do projeto
# Observação: mantenha um requirements.txt no diretório raiz do projeto
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia o código (o docker-compose irá montar volumes em ambiente de desenvolvimento)
COPY src /app/src

# O comando/entrypoint será definido por serviço no docker-compose