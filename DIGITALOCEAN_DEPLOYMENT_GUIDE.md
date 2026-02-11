# 🚀 Django Project: Render → DigitalOcean Migration Guide

Complete guide to migrate **SkillConnect** from Render to DigitalOcean

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Option 1: DigitalOcean App Platform (Recommended)](#option-1-digitalocean-app-platform)
3. [Option 2: DigitalOcean Droplet (VPS)](#option-2-digitalocean-droplet)
4. [Database Migration](#database-migration)
5. [Domain Configuration](#domain-configuration)
6. [Post-Deployment](#post-deployment)

---

## Prerequisites

### 1. DigitalOcean Account Setup
```bash
# Sign up at: https://www.digitalocean.com
# Get $200 credit for 60 days (new users)
```

### 2. Install DigitalOcean CLI (doctl)
```bash
# Windows (PowerShell)
winget install DigitalOcean.Doctl

# Verify installation
doctl version
```

### 3. Authenticate doctl
```bash
# Create API token: https://cloud.digitalocean.com/account/api/tokens
doctl auth init

# Verify authentication
doctl account get
```

---

## Option 1: DigitalOcean App Platform (Recommended) 🌟

**Best for:** Production-ready deployment similar to Render/Heroku

### Step 1: Create App Spec File

Create `app.yaml` in your project root:

```yaml
name: skillconnect-backend
region: nyc
databases:
  - name: skillconnect-db
    engine: PG
    version: "15"
    production: false
    cluster_name: skillconnect-cluster

services:
  - name: web
    github:
      repo: your-username/skillconnect-backend
      branch: main
      deploy_on_push: true
    
    build_command: |
      pip install -r requirements.txt
      python manage.py collectstatic --no-input
    
    run_command: gunicorn core.wsgi:application --timeout 120 --workers 2 --threads 2
    
    instance_count: 1
    instance_size_slug: basic-xxs
    
    http_port: 8000
    
    routes:
      - path: /
    
    health_check:
      http_path: /
      initial_delay_seconds: 30
      period_seconds: 10
    
    envs:
      - key: DEBUG
        value: "False"
      
      - key: PYTHON_VERSION
        value: "3.12.0"
      
      - key: SECRET_KEY
        scope: RUN_AND_BUILD_TIME
        type: SECRET
      
      - key: GROQ_API_KEY
        scope: RUN_AND_BUILD_TIME
        type: SECRET
      
      - key: DATABASE_URL
        scope: RUN_AND_BUILD_TIME
        type: SECRET
      
      - key: ALLOWED_HOSTS
        value: ".ondigitalocean.app,skillconnect.dev,www.skillconnect.dev"
      
      - key: DJANGO_SETTINGS_MODULE
        value: "core.settings"

jobs:
  - name: migrate
    kind: PRE_DEPLOY
    run_command: |
      python manage.py migrate
      python create_admin.py
      python add_jobs.py
    
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        type: SECRET
```

### Step 2: Deploy Using doctl

```bash
# Navigate to project directory
cd e:\skillconnect-backend

# Create app from spec
doctl apps create --spec app.yaml

# Get app ID
doctl apps list

# Monitor deployment
doctl apps logs <APP_ID> --follow

# Update app (after changes)
doctl apps update <APP_ID> --spec app.yaml
```

### Step 3: Deploy via Web UI (Alternative)

1. Go to: https://cloud.digitalocean.com/apps
2. Click **"Create App"**
3. **Source:**
   - Connect GitHub repository
   - Select `skillconnect-backend`
   - Branch: `main`
4. **Configure Web Service:**
   - Name: `skillconnect-backend`
   - Build Command:
     ```bash
     pip install -r requirements.txt
     python manage.py collectstatic --no-input
     ```
   - Run Command:
     ```bash
     gunicorn core.wsgi:application --timeout 120 --workers 2 --threads 2
     ```
   - HTTP Port: `8000`
5. **Add Database:**
   - Click "Add Resource" → "Database"
   - Select PostgreSQL 15
   - Plan: Development (Free) or Production ($15/mo)
6. **Environment Variables:**
   ```
   DEBUG=False
   SECRET_KEY=<generate-strong-key>
   GROQ_API_KEY=<your-api-key>
   ALLOWED_HOSTS=.ondigitalocean.app,skillconnect.dev
   DATABASE_URL=${skillconnect-db.DATABASE_URL}
   ```
7. Click **"Create Resources"**

---

## Option 2: DigitalOcean Droplet (VPS) ⚙️

**Best for:** Full control, cost-effective for multiple projects

### Step 1: Create Droplet

```bash
# Create Ubuntu 22.04 droplet
doctl compute droplet create skillconnect-server \
  --region nyc1 \
  --size s-1vcpu-1gb \
  --image ubuntu-22-04-x64 \
  --ssh-keys <your-ssh-key-id>

# Get droplet IP
doctl compute droplet list
```

**Or via Web UI:**
1. Go to: https://cloud.digitalocean.com/droplets
2. Click **"Create Droplet"**
3. **Choose Region:** New York (NYC1)
4. **Choose Image:** Ubuntu 22.04 LTS
5. **Choose Size:** Basic $6/mo (1 GB RAM)
6. **Authentication:** SSH keys or password
7. Click **"Create Droplet"**

### Step 2: Initial Server Setup

```bash
# SSH into droplet
ssh root@<your-droplet-ip>

# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib supervisor git ufw

# Create app user
adduser skillconnect
usermod -aG sudo skillconnect

# Switch to app user
su - skillconnect
```

### Step 3: Setup PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

-- Create database and user
CREATE DATABASE skillconnect;
CREATE USER skillconnect WITH PASSWORD 'your_strong_password';
ALTER ROLE skillconnect SET client_encoding TO 'utf8';
ALTER ROLE skillconnect SET default_transaction_isolation TO 'read committed';
ALTER ROLE skillconnect SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE skillconnect TO skillconnect;
\q
```

### Step 4: Deploy Django Application

```bash
# Clone repository
cd /home/skillconnect
git clone https://github.com/your-username/skillconnect-backend.git
cd skillconnect-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
```

Add to `.env`:
```env
DEBUG=False
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://skillconnect:your_strong_password@localhost/skillconnect
ALLOWED_HOSTS=your-droplet-ip,skillconnect.dev,www.skillconnect.dev
GROQ_API_KEY=your-groq-api-key
```

```bash
# Load environment variables
source .env

# Run migrations
python manage.py collectstatic --no-input
python manage.py migrate
python create_admin.py
python add_jobs.py

# Test gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Step 5: Configure Gunicorn with Supervisor

```bash
# Create gunicorn socket
sudo nano /etc/supervisor/conf.d/skillconnect.conf
```

Add:
```ini
[program:skillconnect]
directory=/home/skillconnect/skillconnect-backend
command=/home/skillconnect/skillconnect-backend/venv/bin/gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
user=skillconnect
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/skillconnect/gunicorn.log
environment=PATH="/home/skillconnect/skillconnect-backend/venv/bin"
```

```bash
# Create log directory
sudo mkdir -p /var/log/skillconnect

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status skillconnect
```

### Step 6: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/skillconnect
```

Add:
```nginx
server {
    listen 80;
    server_name your-droplet-ip skillconnect.dev www.skillconnect.dev;

    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/skillconnect/skillconnect-backend/staticfiles/;
    }

    location /media/ {
        alias /home/skillconnect/skillconnect-backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/skillconnect /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# Enable on boot
sudo systemctl enable nginx
```

### Step 7: Setup Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### Step 8: Install SSL Certificate (Optional but Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d skillconnect.dev -d www.skillconnect.dev

# Auto-renewal test
sudo certbot renew --dry-run
```

---

## Database Migration 🗄️

### Option A: Export from Render

```bash
# Get database credentials from Render dashboard
# Install PostgreSQL client locally

# Export data
pg_dump -h <render-host> -U <render-user> -d <render-db> > skillconnect_backup.sql

# Import to DigitalOcean
psql -h <do-host> -U <do-user> -d <do-db> < skillconnect_backup.sql
```

### Option B: Use Django's dumpdata/loaddata

```bash
# On Render (or locally connected to Render DB)
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data.json

# On DigitalOcean
python manage.py loaddata data.json
```

---

## Domain Configuration 🌐

### Update DNS Settings

1. Go to your domain registrar
2. Update A records:
   ```
   Type  Name     Value
   ────────────────────────────────
   A     @        <your-droplet-ip or app-platform-ip>
   A     www      <your-droplet-ip or app-platform-ip>
   A     api      <your-droplet-ip or app-platform-ip>
   ```

### Update Django Settings

Update [core/settings.py](core/settings.py):

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.ondigitalocean.app',  # For App Platform
    'your-droplet-ip',      # For Droplet
    'skillconnect.dev',
    'www.skillconnect.dev',
    'api.skillconnect.dev',
]

CSRF_TRUSTED_ORIGINS = [
    'https://skillconnect.dev',
    'https://www.skillconnect.dev',
    'https://*.ondigitalocean.app',
]
```

---

## Post-Deployment Checklist ✅

### 1. Verify Deployment

```bash
# Test API endpoints
curl https://your-app.ondigitalocean.app/
curl https://your-app.ondigitalocean.app/api/

# Check admin panel
open https://your-app.ondigitalocean.app/admin/
```

### 2. Monitor Logs

**App Platform:**
```bash
doctl apps logs <APP_ID> --follow
doctl apps logs <APP_ID> --type run
```

**Droplet:**
```bash
sudo tail -f /var/log/skillconnect/gunicorn.log
sudo tail -f /var/log/nginx/error.log
```

### 3. Setup Monitoring (Optional)

```bash
# Install monitoring agent
curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash
```

### 4. Setup Automated Backups

**For App Platform Database:**
- Enabled automatically in DigitalOcean dashboard

**For Droplet:**
```bash
# Create backup script
nano /home/skillconnect/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/skillconnect/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U skillconnect skillconnect > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /home/skillconnect/skillconnect-backend/media

# Keep only last 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

```bash
# Make executable
chmod +x /home/skillconnect/backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
0 2 * * * /home/skillconnect/backup.sh
```

### 5. Environment Variables Security

**Never commit:**
- `.env` files
- Secret keys
- API keys
- Database passwords

**Add to `.gitignore`:**
```
.env
*.env
local_settings.py
```

---

## Cost Comparison 💰

| Feature | Render (Free) | DO App Platform | DO Droplet |
|---------|---------------|-----------------|------------|
| Web Service | Free | $5/mo | - |
| Database | Free | $15/mo | Included |
| Droplet | - | - | $6/mo |
| **Total** | **$0** | **$20/mo** | **$6/mo** |

**Recommendation:**
- **Development:** DigitalOcean Droplet ($6/mo)
- **Production:** DigitalOcean App Platform ($20/mo)

---

## Troubleshooting 🔧

### Common Issues

**1. Static files not loading:**
```bash
python manage.py collectstatic --clear --no-input
sudo supervisorctl restart skillconnect
sudo systemctl restart nginx
```

**2. Database connection errors:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U skillconnect -d skillconnect
```

**3. Permission errors:**
```bash
# Fix ownership
sudo chown -R skillconnect:skillconnect /home/skillconnect/skillconnect-backend
chmod -R 755 /home/skillconnect/skillconnect-backend
```

**4. Memory issues (for $6 droplet):**
```bash
# Add swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Useful Commands 📝

### App Platform
```bash
# List apps
doctl apps list

# Get app info
doctl apps get <APP_ID>

# View logs
doctl apps logs <APP_ID> --follow

# List deployments
doctl apps list-deployments <APP_ID>

# Create deployment
doctl apps create-deployment <APP_ID>

# Delete app
doctl apps delete <APP_ID>
```

### Droplet Management
```bash
# List droplets
doctl compute droplet list

# Get droplet info
doctl compute droplet get <DROPLET_ID>

# Restart droplet
doctl compute droplet-action reboot <DROPLET_ID>

# Resize droplet
doctl compute droplet-action resize <DROPLET_ID> --size s-2vcpu-2gb

# Enable backups
doctl compute droplet-action enable-backups <DROPLET_ID>
```

### Django Management
```bash
# SSH into droplet/app
# Then run:

# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static
python manage.py collectstatic

# Django shell
python manage.py shell

# Check deployment
python manage.py check --deploy
```

---

## Next Steps 🎯

1. ✅ Choose deployment method (App Platform or Droplet)
2. ✅ Setup DigitalOcean account
3. ✅ Deploy application
4. ✅ Migrate database
5. ✅ Configure domain
6. ✅ Setup SSL certificate
7. ✅ Configure monitoring
8. ✅ Test all endpoints
9. ✅ Update documentation

---

## Support Resources 📚

- **DigitalOcean Docs:** https://docs.digitalocean.com
- **Community Tutorials:** https://www.digitalocean.com/community/tutorials
- **Support:** https://www.digitalocean.com/support
- **Status:** https://status.digitalocean.com

---

## Author
**Migration Guide by:** GitHub Copilot  
**Date:** February 12, 2026  
**Project:** SkillConnect Backend

---

**Happy Deploying! 🚀**
