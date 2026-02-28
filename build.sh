#!/usr/bin/env bash
# Build Script (Local XAMPP + Cloud Deploy)

set -o errexit

pip install -r requirements.txt

# Collectstatic with SQLite (inline env var - set BEFORE Python reads settings)
DATABASE_URL="sqlite:///tmp/temp.db" python manage.py collectstatic --no-input --clear

# Migrate uses real DATABASE_URL from environment or MySQL default
python manage.py migrate
python create_admin.py
python add_jobs.py
