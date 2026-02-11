# 🌊 DigitalOcean Deployment Guide - SkillConnect

## 📋 Overview

This guide will help you deploy SkillConnect Backend on **DigitalOcean App Platform** - similar to Render but with more features.

---

## 💰 Estimated Cost

| Service | Cost/Month |
|---------|------------|
| App Platform (Basic) | $5 |
| PostgreSQL Database | $7 |
| **Total** | **~$12/month** |

*Note: DigitalOcean also has $200 free credits for new users!*

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Code

```bash
# 1. Commit all changes
git add .
git commit -m "Add DigitalOcean deployment config"
git push origin main
```

### Step 2: Create DigitalOcean Account

1. Go to [DigitalOcean](https://www.digitalocean.com/)
2. Sign up (get $200 free credits!)
3. Add billing info

### Step 3: Create App

**Option A: Using Dashboard (Easy)**

1. Go to **Apps** > **Create App**
2. Select **GitHub** as source
3. Authorize DigitalOcean to access your repo
4. Select `skillconnect-backend` repository
5. Branch: `main`
6. Click **Next**

**Option B: Using CLI**

```bash
# Install doctl CLI
winget install DigitalOcean.Doctl

# Login
doctl auth init

# Create app from config
doctl apps create --spec .do/app.yaml
```

### Step 4: Configure Database

1. During app creation, add **Dev Database** component
2. Select **PostgreSQL 16**
3. Name: `skillconnect-db`
4. Plan: Dev Database ($7/month)

### Step 5: Set Environment Variables

In the App Settings, add these variables:

| Variable | Value | Type |
|----------|-------|------|
| `SECRET_KEY` | Generate random string | Secret |
| `DEBUG` | `False` | Plain |
| `GROQ_API_KEY` | Your API key from console.groq.com | Secret |
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary cloud name | Plain |
| `CLOUDINARY_API_KEY` | Your API key | Secret |
| `CLOUDINARY_API_SECRET` | Your API secret | Secret |

**Generate Secret Key:**
```python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Step 6: Deploy

1. Click **Create Resources**
2. Wait for build (~5-10 minutes)
3. Your app will be live at: `https://skillconnect-api-xxxxx.ondigitalocean.app`

---

## 🔗 After Deployment

### Get Your App URL

```bash
# Using CLI
doctl apps list
```

Or check in Dashboard > Apps > Your App > **App URL**

### Run Migrations (if needed)

```bash
# Access console via CLI
doctl apps console YOUR_APP_ID

# Run migrations
python manage.py migrate
```

### View Logs

```bash
doctl apps logs YOUR_APP_ID --type run
```

---

## ⚙️ Custom Domain Setup

1. Go to App Settings > **Domains**
2. Add your domain: `api.skillconnect.dev`
3. Update DNS:
   - Add CNAME record: `api` → `your-app-xxxxx.ondigitalocean.app`
   - Or use DigitalOcean DNS

---

## 🔄 Auto-Deploy

Already configured! Every `git push` to `main` will auto-deploy.

```bash
git add .
git commit -m "New feature"
git push origin main  # Auto-deploys!
```

---

## 🆚 Render vs DigitalOcean Comparison

| Feature | Render | DigitalOcean |
|---------|--------|--------------|
| Free Tier | Yes (limited) | $200 credits |
| Pricing | Starts $7 | Starts $5 |
| Database | PostgreSQL | PostgreSQL |
| Location | US, EU | US, EU, Asia |
| Auto-deploy | ✅ | ✅ |
| Custom Domain | ✅ | ✅ |
| SSL | Free | Free |

---

## 🛠️ Troubleshooting

### Build Fails

```bash
# Check build logs
doctl apps logs YOUR_APP_ID --type build
```

### Database Connection Error

Make sure `DATABASE_URL` env variable is linked to the database component.

### Static Files Not Loading

Ensure `whitenoise` is in requirements.txt and middleware is configured.

---

## 📞 Support

- DigitalOcean Docs: https://docs.digitalocean.com/products/app-platform/
- Community: https://www.digitalocean.com/community

---

**Happy Deploying! 🚀**
