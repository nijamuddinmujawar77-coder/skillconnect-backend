#!/usr/bin/env bash
# Build Script (Render / DigitalOcean App Platform)

set -o errexit

pip install -r requirements.txt

# Preserve original DATABASE_URL
ORIGINAL_DB_URL=$DATABASE_URL

# Use SQLite for collectstatic (doesn't need server connection)
export DATABASE_URL="sqlite:///tmp/build.db"
python manage.py collectstatic --no-input --clear

# Restore real DATABASE_URL for migrate
export DATABASE_URL=$ORIGINAL_DB_URL
python manage.py migrate
python create_admin.py
python add_jobs.py
