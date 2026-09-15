#!/bin/sh
set -e

echo "applying migrations..."
python manage.py migrate --noinput #--skip-checks

echo "collecting static files..."
python manage.py collectstatic --noinput

echo "starting the application... with debugpy"
# python -X frozen_modules=off -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000
python -X frozen_modules=off -m debugpy --listen 0.0.0.0:5678 -m uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload 