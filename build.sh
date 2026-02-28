#!/usr/bin/env bash
# Build Script (Local XAMPP + Cloud Deploy)

set -o errexit

pip install -r requirements.txt

# Collectstatic only (doesn't need DB connection)
DATABASE_URL="sqlite:///tmp/temp.db" python manage.py collectstatic --no-input --clear

echo "✅ Build complete. Migrations will run at startup."
