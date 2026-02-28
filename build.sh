#!/usr/bin/env bash
# Build Script (Render / DigitalOcean App Platform)

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input --clear
python manage.py migrate
python create_admin.py
python add_jobs.py
