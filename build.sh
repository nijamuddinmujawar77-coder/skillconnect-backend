#!/usr/bin/env bash
# Build Script (Local XAMPP + Cloud Deploy)

set -o errexit

pip install -r requirements.txt

# Collectstatic with SQLite (doesn't need real DB)
DATABASE_URL="sqlite:///tmp/temp.db" python manage.py collectstatic --no-input --clear

# Migrations need real DB - settings.py will handle fallback
python manage.py migrate
python create_admin.py
python add_jobs.py
