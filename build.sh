#!/usr/bin/env bash
# Render Build Script

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python create_admin.py
python add_jobs.py
