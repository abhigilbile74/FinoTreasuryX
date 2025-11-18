#!/bin/bash
set -o errexit
set -o pipefail

echo "📦 Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "🗂 Collecting static files..."
python manage.py collectstatic --no-input

echo "🛠 Applying migrations..."
python manage.py migrate --no-input

if [ "$CREATE_SUPERUSER" = "true" ]; then
    python manage.py createsuperuser --no-input || true
fi

echo "🚀 Starting Gunicorn..."
gunicorn Finance.asgi:application \
    -k uvicorn.workers.UvicornWorker \
    --workers 1 \
    --bind 0.0.0.0:$PORT \
    --timeout 60
