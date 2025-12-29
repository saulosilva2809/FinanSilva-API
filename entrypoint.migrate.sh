#!/bin/sh
set -e

echo "🧠 Aplicando migrations (container único)..."
python manage.py migrate --noinput

echo "🚀 Subindo serviço web..."
exec "$@"
