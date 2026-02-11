# 📋 Render → DigitalOcean Migration Checklist

## Pre-Migration Preparation

### 1. Backup Everything ✅
- [ ] Export Render PostgreSQL database
  ```bash
  # Get connection string from Render dashboard
  pg_dump -h <render-host> -U <user> -d <database> > skillconnect_backup.sql
  ```
- [ ] Download all media files
- [ ] Export environment variables from Render
- [ ] Save current `requirements.txt`
- [ ] Document custom configurations

### 2. DigitalOcean Account Setup ✅
- [ ] Create DigitalOcean account
  - URL: https://www.digitalocean.com
  - Get $200 credit (new users)
- [ ] Add payment method
- [ ] Verify email
- [ ] Enable 2FA (recommended)

### 3. Install Tools ✅
- [ ] Install doctl (DigitalOcean CLI)
  ```powershell
  winget install DigitalOcean.Doctl
  ```
- [ ] Authenticate doctl
  ```bash
  doctl auth init
  doctl account get
  ```
- [ ] Install PostgreSQL client (for database migration)
  ```powershell
  winget install PostgreSQL.PostgreSQL
  ```

---

## Choose Your Deployment Method

### Option A: App Platform (Recommended for Beginners) ✅
- [ ] Review pricing: $5/mo web + $15/mo database = $20/mo
- [ ] Decide if budget is acceptable
- [ ] Proceed to "App Platform Deployment" section

### Option B: Droplet (Recommended for Cost Savings) ✅
- [ ] Review pricing: $6/mo total
- [ ] Confirm you have Linux/DevOps knowledge
- [ ] Proceed to "Droplet Deployment" section

---

## App Platform Deployment (Option A)

### 1. Prepare Files ✅
- [ ] Update [app.yaml](app.yaml) with your GitHub repository
  ```yaml
  github:
    repo: your-username/skillconnect-backend  # UPDATE THIS
    branch: main
  ```
- [ ] Update environment variables in `app.yaml`
- [ ] Generate new `SECRET_KEY`
  ```python
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  ```
- [ ] Add your API keys (GROQ_API_KEY, etc.)

### 2. Create Database ✅
- [ ] Go to: https://cloud.digitalocean.com/databases
- [ ] Click "Create Database Cluster"
- [ ] Select PostgreSQL 15
- [ ] Choose plan: Development ($15/mo) or Production
- [ ] Select region: New York (NYC1)
- [ ] Name: `skillconnect-db`
- [ ] Create database

### 3. Deploy Application ✅
- [ ] Method 1: Using doctl
  ```bash
  cd e:\skillconnect-backend
  doctl apps create --spec app.yaml
  ```
- [ ] OR Method 2: Using Web UI
  - Go to: https://cloud.digitalocean.com/apps
  - Click "Create App"
  - Connect GitHub repository
  - Configure build/run commands
  - Add environment variables
  - Create app

### 4. Configure Environment ✅
- [ ] Add environment variables in DigitalOcean dashboard:
  - `DEBUG=False`
  - `SECRET_KEY=<your-secret-key>`
  - `DATABASE_URL=<auto-from-database>`
  - `GROQ_API_KEY=<your-api-key>`
  - `ALLOWED_HOSTS=.ondigitalocean.app,skillconnect.dev`

### 5. Monitor Deployment ✅
- [ ] Check build logs
  ```bash
  doctl apps list
  doctl apps logs <APP_ID> --follow
  ```
- [ ] Wait for deployment to complete
- [ ] Note the app URL: `https://skillconnect-backend-xxxxx.ondigitalocean.app`

---

## Droplet Deployment (Option B)

### 1. Create Droplet ✅
- [ ] Go to: https://cloud.digitalocean.com/droplets
- [ ] Click "Create Droplet"
- [ ] Select image: Ubuntu 22.04 LTS
- [ ] Choose plan: Basic $6/mo (1GB RAM)
- [ ] Select region: New York (NYC1)
- [ ] Add SSH keys or password authentication
- [ ] Hostname: `skillconnect-server`
- [ ] Create droplet
- [ ] Note the droplet IP address

### 2. Initial Server Setup ✅
- [ ] SSH into droplet
  ```bash
  ssh root@<your-droplet-ip>
  ```
- [ ] Update system
  ```bash
  apt update && apt upgrade -y
  ```
- [ ] Install required packages
  ```bash
  apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib supervisor git ufw
  ```
- [ ] Create application user
  ```bash
  adduser skillconnect
  usermod -aG sudo skillconnect
  ```

### 3. Setup PostgreSQL ✅
- [ ] Create database and user
  ```bash
  sudo -u postgres psql
  ```
  ```sql
  CREATE DATABASE skillconnect;
  CREATE USER skillconnect WITH PASSWORD 'your_strong_password';
  GRANT ALL PRIVILEGES ON DATABASE skillconnect TO skillconnect;
  \q
  ```
- [ ] Test connection
  ```bash
  psql -U skillconnect -d skillconnect
  ```

### 4. Deploy Application ✅
- [ ] Clone repository
  ```bash
  su - skillconnect
  git clone https://github.com/your-username/skillconnect-backend.git
  cd skillconnect-backend
  ```
- [ ] Create virtual environment
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] Install dependencies
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  pip install gunicorn
  ```
- [ ] Create `.env` file
  ```bash
  nano .env
  ```
  Add:
  ```env
  DEBUG=False
  SECRET_KEY=your-secret-key
  DATABASE_URL=postgresql://skillconnect:password@localhost/skillconnect
  ALLOWED_HOSTS=<droplet-ip>,skillconnect.dev
  GROQ_API_KEY=your-api-key
  ```
- [ ] Run migrations
  ```bash
  python manage.py migrate
  python manage.py collectstatic --no-input
  python create_admin.py
  python add_jobs.py
  ```

### 5. Configure Gunicorn ✅
- [ ] Create supervisor config
  ```bash
  sudo nano /etc/supervisor/conf.d/skillconnect.conf
  ```
- [ ] Add configuration (see full guide)
- [ ] Start service
  ```bash
  sudo supervisorctl reread
  sudo supervisorctl update
  sudo supervisorctl status skillconnect
  ```

### 6. Configure Nginx ✅
- [ ] Create Nginx config
  ```bash
  sudo nano /etc/nginx/sites-available/skillconnect
  ```
- [ ] Add configuration (see full guide)
- [ ] Enable site
  ```bash
  sudo ln -s /etc/nginx/sites-available/skillconnect /etc/nginx/sites-enabled/
  sudo nginx -t
  sudo systemctl restart nginx
  ```

### 7. Setup Firewall ✅
- [ ] Configure UFW
  ```bash
  sudo ufw allow OpenSSH
  sudo ufw allow 'Nginx Full'
  sudo ufw enable
  ```

### 8. Install SSL Certificate ✅
- [ ] Install Certbot
  ```bash
  sudo apt install certbot python3-certbot-nginx -y
  ```
- [ ] Get certificate (after DNS configured)
  ```bash
  sudo certbot --nginx -d skillconnect.dev -d www.skillconnect.dev
  ```

---

## Database Migration

### 1. Export from Render ✅
- [ ] Get Render database credentials
- [ ] Export database
  ```bash
  pg_dump -h <render-host> -U <render-user> -d <render-db> -F c -b -v -f skillconnect.backup
  ```
- [ ] Download backup file

### 2. Import to DigitalOcean ✅
- [ ] Get DigitalOcean database credentials
- [ ] Import database
  ```bash
  pg_restore -h <do-host> -U <do-user> -d <do-db> -v skillconnect.backup
  ```
- [ ] OR for SQL file:
  ```bash
  psql -h <do-host> -U <do-user> -d <do-db> < skillconnect_backup.sql
  ```

### 3. Verify Data ✅
- [ ] Check tables exist
  ```bash
  psql -h <do-host> -U <do-user> -d <do-db> -c "\dt"
  ```
- [ ] Verify record counts
  ```sql
  SELECT COUNT(*) FROM accounts_customuser;
  SELECT COUNT(*) FROM jobs_job;
  ```

---

## Domain Configuration

### 1. Update DNS Records ✅
- [ ] Go to your domain registrar
- [ ] Update A records:
  ```
  Type    Name    Value
  ────────────────────────────────────
  A       @       <digitalocean-ip>
  A       www     <digitalocean-ip>
  A       api     <digitalocean-ip>
  ```
- [ ] Set TTL to 300 (5 minutes) for testing
- [ ] Wait for DNS propagation (5-60 minutes)

### 2. Verify DNS ✅
- [ ] Check DNS propagation
  ```bash
  nslookup skillconnect.dev
  nslookup www.skillconnect.dev
  ```
- [ ] Test in browser
  ```
  http://skillconnect.dev
  https://skillconnect.dev
  ```

---

## Testing & Verification

### 1. Test API Endpoints ✅
- [ ] Homepage: `https://your-app.ondigitalocean.app/`
- [ ] Admin: `https://your-app.ondigitalocean.app/admin/`
- [ ] API: `https://your-app.ondigitalocean.app/api/`
- [ ] Jobs: `https://your-app.ondigitalocean.app/api/jobs/`
- [ ] Accounts: `https://your-app.ondigitalocean.app/api/accounts/`

### 2. Test Functionality ✅
- [ ] User registration
- [ ] User login
- [ ] Job posting
- [ ] Job application
- [ ] Resume upload
- [ ] AI services
- [ ] Email notifications

### 3. Performance Testing ✅
- [ ] Load time < 2s
- [ ] API response time < 500ms
- [ ] Database queries optimized
- [ ] Static files loading correctly

### 4. Security Check ✅
- [ ] HTTPS working
- [ ] DEBUG=False in production
- [ ] SECRET_KEY is strong and unique
- [ ] Database not publicly accessible
- [ ] Admin panel is secure
- [ ] CORS configured correctly

---

## Monitoring Setup

### 1. Application Monitoring ✅
- [ ] Setup DigitalOcean monitoring
- [ ] Configure alerts:
  - CPU usage > 80%
  - Memory usage > 80%
  - Disk usage > 80%
  - App downtime

### 2. Log Monitoring ✅
- [ ] App Platform: `doctl apps logs <APP_ID> --follow`
- [ ] Droplet:
  ```bash
  sudo tail -f /var/log/skillconnect/gunicorn.log
  sudo tail -f /var/log/nginx/error.log
  ```

### 3. Uptime Monitoring ✅
- [ ] Use UptimeRobot or similar
- [ ] Add endpoint: `https://skillconnect.dev`
- [ ] Configure email alerts

---

## Backup Configuration

### 1. Database Backups ✅
- [ ] App Platform: Enable automatic backups
- [ ] Droplet: Setup cron job
  ```bash
  crontab -e
  # Add: 0 2 * * * /home/skillconnect/backup.sh
  ```

### 2. Media Files Backup ✅
- [ ] Configure DigitalOcean Spaces (optional)
- [ ] OR setup rsync backup to local

### 3. Code Backup ✅
- [ ] Ensure Git repository is up-to-date
- [ ] Tag release version
  ```bash
  git tag -a v1.0.0 -m "Production deployment"
  git push origin v1.0.0
  ```

---

## Final Steps

### 1. Update Documentation ✅
- [ ] Update [README.md](README.md) with new deployment info
- [ ] Document environment variables
- [ ] Update deployment URLs
- [ ] Add troubleshooting notes

### 2. Notify Team/Users ✅
- [ ] Send migration announcement
- [ ] Update social media links
- [ ] Update documentation URLs
- [ ] Inform stakeholders

### 3. Monitor for 24-48 Hours ✅
- [ ] Check error logs daily
- [ ] Monitor performance metrics
- [ ] Address any issues immediately
- [ ] Collect user feedback

### 4. Cleanup Render ✅
- [ ] Wait 48-72 hours before cleanup
- [ ] Verify all data migrated
- [ ] Export final logs
- [ ] Cancel Render subscription (if paid)
- [ ] Delete Render app (optional)

---

## Rollback Plan (If Needed)

### Emergency Rollback ✅
- [ ] Revert DNS to Render
  ```
  A    @      <render-ip>
  ```
- [ ] Wait for DNS propagation
- [ ] Identify and fix issue
- [ ] Re-attempt migration

---

## Success Criteria

### Migration is Complete When: ✅
- [x] Application accessible on new URL
- [x] All functionality working
- [x] Database fully migrated
- [x] SSL certificate active
- [x] Performance acceptable
- [x] Monitoring active
- [x] Backups configured
- [x] No critical errors in logs
- [x] Users can access normally
- [x] Team trained on new platform

---

## 🎉 Congratulations!

You've successfully migrated from Render to DigitalOcean!

### Next Steps:
1. Monitor for 1 week
2. Optimize performance
3. Setup CI/CD (optional)
4. Configure advanced monitoring
5. Plan for scaling

---

## 📚 Resources

- **Full Guide:** [DIGITALOCEAN_DEPLOYMENT_GUIDE.md](DIGITALOCEAN_DEPLOYMENT_GUIDE.md)
- **Quick Reference:** [DIGITALOCEAN_QUICKSTART.md](DIGITALOCEAN_QUICKSTART.md)
- **Comparison:** [RENDER_VS_DIGITALOCEAN.md](RENDER_VS_DIGITALOCEAN.md)
- **DigitalOcean Docs:** https://docs.digitalocean.com
- **Community:** https://www.digitalocean.com/community

---

**Migration Date:** _______________  
**Completed By:** _______________  
**Platform:** [ ] App Platform  [ ] Droplet  
**Status:** [ ] In Progress  [ ] Completed  [ ] Rolled Back

---

**Last Updated:** February 12, 2026  
**Version:** 1.0
