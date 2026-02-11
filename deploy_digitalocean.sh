#!/bin/bash
# DigitalOcean Deployment Script
# Usage: ./deploy_digitalocean.sh [app|droplet]

set -e

echo "🚀 SkillConnect - DigitalOcean Deployment Script"
echo "================================================"

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "❌ Error: doctl is not installed"
    echo "Install: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check authentication
if ! doctl account get &> /dev/null; then
    echo "❌ Error: Not authenticated with DigitalOcean"
    echo "Run: doctl auth init"
    exit 1
fi

echo "✅ doctl found and authenticated"
echo ""

# Get deployment type
DEPLOY_TYPE=${1:-"app"}

if [ "$DEPLOY_TYPE" == "app" ]; then
    echo "📦 Deploying to DigitalOcean App Platform..."
    echo ""
    
    # Check if app.yaml exists
    if [ ! -f "app.yaml" ]; then
        echo "❌ Error: app.yaml not found"
        exit 1
    fi
    
    # Update GitHub repo in app.yaml
    echo "⚠️  Remember to update 'github.repo' in app.yaml with your repository"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    
    # Create or update app
    if [ -z "$APP_ID" ]; then
        echo "Creating new app..."
        doctl apps create --spec app.yaml
    else
        echo "Updating app $APP_ID..."
        doctl apps update $APP_ID --spec app.yaml
    fi
    
    echo ""
    echo "✅ Deployment initiated!"
    echo "Monitor logs: doctl apps list"
    
elif [ "$DEPLOY_TYPE" == "droplet" ]; then
    echo "🖥️  Setting up DigitalOcean Droplet..."
    echo ""
    
    # Get SSH key ID
    echo "Available SSH keys:"
    doctl compute ssh-key list
    echo ""
    read -p "Enter SSH Key ID: " SSH_KEY_ID
    
    # Create droplet
    echo "Creating droplet..."
    doctl compute droplet create skillconnect-server \
        --region nyc1 \
        --size s-1vcpu-1gb \
        --image ubuntu-22-04-x64 \
        --ssh-keys $SSH_KEY_ID \
        --wait
    
    # Get droplet IP
    DROPLET_IP=$(doctl compute droplet list --format PublicIPv4 --no-header)
    
    echo ""
    echo "✅ Droplet created!"
    echo "IP Address: $DROPLET_IP"
    echo ""
    echo "Next steps:"
    echo "1. SSH into droplet: ssh root@$DROPLET_IP"
    echo "2. Follow the manual setup guide in DIGITALOCEAN_DEPLOYMENT_GUIDE.md"
    
else
    echo "❌ Invalid deployment type: $DEPLOY_TYPE"
    echo "Usage: ./deploy_digitalocean.sh [app|droplet]"
    exit 1
fi

echo ""
echo "📚 Full guide: DIGITALOCEAN_DEPLOYMENT_GUIDE.md"
