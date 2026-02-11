# 🚀 DigitalOcean - Simple Deployment Guide

## Bas Teen Steps! 😊

### **Step 1: DigitalOcean Account Banao** (5 minutes)
1. Jao: https://www.digitalocean.com
2. Sign up karo (GitHub se login kar sakte ho)
3. Credit card add karo → Milega **$200 FREE credit** for 60 days!

### **Step 2: doctl Install Karo** (2 minutes)

PowerShell me ye command run karo:
```powershell
winget install DigitalOcean.Doctl
```

### **Step 3: Deploy Karo!** (5 minutes)

#### 3a. API Token banao:
1. Jao: https://cloud.digitalocean.com/account/api/tokens
2. "Generate New Token" click karo
3. Name: `SkillConnect`
4. Full Access select karo
5. Token **copy karo** (sirf ek baar dikhega!)

#### 3b. Terminal me ye commands run karo:
```powershell
# Navigate to project
cd e:\skillconnect-backend

# Authenticate (paste your token when asked)
doctl auth init

# Push code to GitHub
git add .
git commit -m "Ready for DigitalOcean deployment"
git push origin main

# Deploy to DigitalOcean App Platform
doctl apps create --spec app.yaml
```

#### 3c. Monitor deployment:
```powershell
# Check app status
doctl apps list

# View logs (replace YOUR_APP_ID from above command)
doctl apps logs YOUR_APP_ID --follow
```

---

## ✅ Deployment Complete!

5-10 minutes mein aapka app live hoga:
```
https://skillconnect-backend-xxxxx.ondigitalocean.app
```

---

## 💰 Cost

- Web Service: **$5/month**
- PostgreSQL Database: **$15/month**
- **Total: $20/month**

(First 60 days FREE with $200 credit!)

---

## 🔧 Environment Variables (App Dashboard me set karo)

DigitalOcean dashboard me jao aur ye variables add karo:

1. **SECRET_KEY** → Generate karo (dashboard me encrypt option hai)
2. **GROQ_API_KEY** → Apni API key dalo
3. **DEBUG** → `False` (already set hai)
4. **DATABASE_URL** → Auto-set (database se link hoga)

---

## 📱 Domain Connect Karna Hai?

1. DigitalOcean app settings me jao
2. "Domains" tab click karo
3. Apna domain add karo: `skillconnect.dev`
4. DNS records update karo (instructions milenge)

---

## 🆘 Problem Aaye?

**Check logs:**
```powershell
doctl apps logs YOUR_APP_ID --follow
```

**Restart app:**
```powershell
doctl apps create-deployment YOUR_APP_ID
```

**View in browser:**
```
https://cloud.digitalocean.com/apps
```

---

## 🎉 That's It!

Itna simple hai! Questions? Just ask! 😊

---

**Quick Links:**
- Dashboard: https://cloud.digitalocean.com/apps
- Docs: https://docs.digitalocean.com/products/app-platform/
- Support: https://www.digitalocean.com/support
