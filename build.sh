#!/bin/bash
set -o errexit
set -o pipefail

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗂 Collecting static files..."
# Comment this to skip static collection if not needed
python manage.py collectstatic --no-input --clear

echo "🛠 Applying migrations..."
python manage.py migrate --no-input

echo "🚀 Starting Gunicorn (FAST MODE)..."
gunicorn Finance.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:$PORT \
  --workers 1 \
  --timeout 0
