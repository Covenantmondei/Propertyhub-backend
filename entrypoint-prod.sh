#!/bin/sh
set -e

echo "applying migrations..."
python manage.py migrate --noinput #--skip-checks

echo "collecting static files..."
python manage.py collectstatic --noinput


echo "starting with gunicorn + uvicorn workers"
gunicorn config.asgi:application --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000