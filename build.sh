#!/bin/bash
set -o errexit
set -o pipefail

echo "⏳ Waiting for PostgreSQL..."
until python - <<END
import os, psycopg2
conn = psycopg2.connect(os.environ["DATABASE_URL"])
conn.close()
END
do
  sleep 3
done

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗂 Collecting static files..."
python manage.py collectstatic --no-input

echo "🛠 Running migrations..."
python manage.py migrate

if [ "$CREATE_SUPERUSER" = "true" ]; then
    python manage.py createsuperuser --no-input || true
fi

echo "✅ All setup done, starting Gunicorn..."
gunicorn Finance.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 2 --timeout 120
