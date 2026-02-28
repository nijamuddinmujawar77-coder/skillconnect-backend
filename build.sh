#!/usr/bin/env bash
# Build Script (Local XAMPP + Cloud Deploy)

set -o errexit

pip install -r requirements.txt

# Collectstatic: Temporarily use SQLite (no server needed)
ORIGINAL_DB=$DATABASE_URL
export DATABASE_URL="sqlite:///tmp/collectstatic_temp.db"
python manage.py collectstatic --no-input --clear

# Restore real DB config for migrate/admin/jobs
# Cloud: PostgreSQL via DATABASE_URL
# Local: MySQL via settings.py default (when DATABASE_URL empty)
export DATABASE_URL=$ORIGINAL_DB

python manage.py migrate
python create_admin.py
python add_jobs.py
