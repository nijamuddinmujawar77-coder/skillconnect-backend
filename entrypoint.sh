#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Creating admin user..."
python create_admin.py || true

echo "Adding initial jobs..."
python add_jobs.py || true

echo "Starting Gunicorn server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --timeout 120 --workers 2 --threads 2
