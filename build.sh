#!/usr/bin/env bash
# Build Script (Render / DigitalOcean App Platform)

set -o errexit

pip install -r requirements.txt

# Set dummy DATABASE_URL if not set (for collectstatic that doesn't need real DB)
if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL="postgresql://dummy:dummy@localhost:5432/dummy"
fi

python manage.py collectstatic --no-input --clear
python manage.py migrate
python create_admin.py
python add_jobs.py
