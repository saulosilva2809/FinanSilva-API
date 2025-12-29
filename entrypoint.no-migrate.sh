#!/bin/sh
set -e

echo "⏳ Aguardando banco estabilizar..."
sleep 5

echo "🚀 Subindo serviço secundário..."
exec "$@"