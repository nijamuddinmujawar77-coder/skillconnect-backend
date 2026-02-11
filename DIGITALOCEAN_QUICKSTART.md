# DigitalOcean Deployment - Quick Reference

## 🚀 Quick Start

### Option 1: App Platform (Easiest)

```bash
# 1. Install doctl
winget install DigitalOcean.Doctl

# 2. Authenticate
doctl auth init

# 3. Update app.yaml with your GitHub repo
# Edit: github.repo → your-username/skillconnect-backend

# 4. Deploy
doctl apps create --spec app.yaml

# 5. Monitor
doctl apps list
doctl apps logs <APP_ID> --follow
```

### Option 2: Droplet (Cost-Effective)

```bash
# 1. Create droplet via web: cloud.digitalocean.com
# 2. Choose Ubuntu 22.04, $6/mo plan
# 3. SSH into server
# 4. Follow manual setup in DIGITALOCEAN_DEPLOYMENT_GUIDE.md
```

---

## 📝 Environment Variables

Set these in DigitalOcean dashboard:

```
DEBUG=False
SECRET_KEY=<generate-strong-key>
DATABASE_URL=<auto-from-db>
GROQ_API_KEY=<your-api-key>
ALLOWED_HOSTS=.ondigitalocean.app,skillconnect.dev
```

---

## 🔗 Important URLs

- **DigitalOcean Console:** https://cloud.digitalocean.com
- **App Platform:** https://cloud.digitalocean.com/apps
- **Droplets:** https://cloud.digitalocean.com/droplets
- **Databases:** https://cloud.digitalocean.com/databases
- **API Tokens:** https://cloud.digitalocean.com/account/api/tokens
- **Documentation:** https://docs.digitalocean.com

---

## 💰 Pricing

| Service | Plan | Price |
|---------|------|-------|
| App Platform | Basic | $5/mo |
| PostgreSQL | Dev | $15/mo |
| Droplet | 1GB RAM | $6/mo |

**Total Cost:**
- App Platform: ~$20/mo
- Droplet: ~$6/mo

---

## 📚 Full Documentation

See [DIGITALOCEAN_DEPLOYMENT_GUIDE.md](DIGITALOCEAN_DEPLOYMENT_GUIDE.md) for complete instructions.

---

## 🆘 Support

**Issues?** Check troubleshooting section in main guide or:
- DigitalOcean Community: https://www.digitalocean.com/community
- Support: https://www.digitalocean.com/support
