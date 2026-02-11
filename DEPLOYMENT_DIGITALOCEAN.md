DigitalOcean App Platform — Deployment checklist (SkillConnect)

Quick summary
- App Platform + Managed PostgreSQL (recommended)
- Repo branch: feature/do-app-deploy (this branch contains DO-ready changes)

1) Create Managed PostgreSQL
- DigitalOcean → Databases → Create a Database Cluster → PostgreSQL
- Choose smallest plan for demo (db-s-1)
- Create database `skillconnect_prod` and a DB user
- Copy the connection string (DATABASE_URL)

2) Create App Platform app
- DigitalOcean → Apps → Create App → Connect GitHub repo
- Select branch: `feature/do-app-deploy` (or `main` after merge)
- Service settings (web):
  - Build command: `pip install -r requirements.txt`
  - Run command: `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`
  - Release command:
      python manage.py migrate --noinput
      python manage.py collectstatic --noinput

3) Add environment variables (DO App → Settings → Environment)
- SECRET_KEY  (strong random)
- DEBUG = False
- DATABASE_URL = postgres://USER:PASS@HOST:PORT/skillconnect_prod
- ALLOWED_HOSTS = your-domain.com,.ondigitalocean.app
- EMAIL_HOST_USER / EMAIL_HOST_PASSWORD (optional)
- RESEND_API_KEY (optional)
- CLOUDINARY_* (optional)

4) Domain & TLS
- In DO App: Add custom domain (e.g. `skillconnect.dev`) and follow instructions
- Add DNS records at your registrar (CNAME to the DO provided hostname)
- Wait for TLS certificate issuance (DO handles Let's Encrypt automatically)

5) Post-deploy verification
- Open https://<your-domain>/ and https://<app>.ondigitalocean.app/
- API smoke: `GET /api/jobs/` should return 200
- Admin: create superuser locally and test login, or use admin panel if migrated

Rollback & Debugging
- If deploy fails: revert to previous deployment in DO UI
- Check logs: DO App → Deployments → View logs
- Common fixes: wrong DATABASE_URL, missing SECRET_KEY, DEBUG left True

Extra notes for demo
- For immediate demo (no DNS): use the DO generated `ondigitalocean.app` domain
- If you prefer, I can perform the DO-side steps if you provide a DO API token (temporary)

Commands you can run locally to verify before pushing:
- python -m venv .venv && .venv\Scripts\activate
- pip install -r requirements.txt
- set SECRET_KEY=dev && set DEBUG=True && set DATABASE_URL=mysql://root:@127.0.0.1:3306/skillconnect_db
- python manage.py migrate
- python manage.py runserver
