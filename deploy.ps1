# DigitalOcean One-Command Deploy Script
# Run this file after installing doctl

Write-Host "🚀 SkillConnect - DigitalOcean Deployment" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if doctl is installed
if (!(Get-Command doctl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ doctl not found! Installing..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Run this command first:" -ForegroundColor Yellow
    Write-Host "winget install DigitalOcean.Doctl" -ForegroundColor Green
    Write-Host ""
    Write-Host "Then run this script again!" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ doctl found!" -ForegroundColor Green
Write-Host ""

# Check authentication
Write-Host "Checking DigitalOcean authentication..." -ForegroundColor Cyan
$authCheck = doctl account get 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not authenticated with DigitalOcean!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Steps to authenticate:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://cloud.digitalocean.com/account/api/tokens" -ForegroundColor White
    Write-Host "2. Click 'Generate New Token'" -ForegroundColor White
    Write-Host "3. Name: 'SkillConnect'" -ForegroundColor White
    Write-Host "4. Select 'Full Access'" -ForegroundColor White
    Write-Host "5. Copy the token" -ForegroundColor White
    Write-Host ""
    Write-Host "Then run: doctl auth init" -ForegroundColor Green
    Write-Host "And paste your token when prompted" -ForegroundColor Green
    Write-Host ""
    exit 1
}

Write-Host "✅ Authenticated!" -ForegroundColor Green
Write-Host ""

# Show account info
Write-Host "Account Info:" -ForegroundColor Cyan
doctl account get
Write-Host ""

# Confirm deployment
Write-Host "Ready to deploy SkillConnect to DigitalOcean!" -ForegroundColor Yellow
Write-Host ""
Write-Host "This will:" -ForegroundColor White
Write-Host "  • Create a PostgreSQL database ($15/mo)" -ForegroundColor White
Write-Host "  • Deploy web service ($5/mo)" -ForegroundColor White
Write-Host "  • Total cost: ~$20/month" -ForegroundColor White
Write-Host "  • You get $200 FREE credit for 60 days!" -ForegroundColor Green
Write-Host ""
$confirm = Read-Host "Continue? (y/n)"

if ($confirm -ne "y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "🚀 Deploying to DigitalOcean..." -ForegroundColor Cyan
Write-Host ""

# Deploy using app.yaml
try {
    $result = doctl apps create --spec app.yaml --format ID --no-header 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        $appId = $result.Trim()
        Write-Host ""
        Write-Host "✅ Deployment started successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "App ID: $appId" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Monitor deployment:" -ForegroundColor Yellow
        Write-Host "  doctl apps logs $appId --follow" -ForegroundColor White
        Write-Host ""
        Write-Host "View in browser:" -ForegroundColor Yellow
        Write-Host "  https://cloud.digitalocean.com/apps/$appId" -ForegroundColor White
        Write-Host ""
        Write-Host "⏳ Deployment will take 5-10 minutes..." -ForegroundColor Cyan
        Write-Host ""
        
        # Ask if they want to follow logs
        $followLogs = Read-Host "Watch deployment logs now? (y/n)"
        if ($followLogs -eq "y") {
            Write-Host ""
            Write-Host "📋 Following deployment logs (Ctrl+C to stop)..." -ForegroundColor Cyan
            Write-Host ""
            doctl apps logs $appId --follow
        } else {
            Write-Host ""
            Write-Host "You can check status later with:" -ForegroundColor Yellow
            Write-Host "  doctl apps get $appId" -ForegroundColor White
            Write-Host ""
        }
        
    } else {
        Write-Host "❌ Deployment failed!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Error: $result" -ForegroundColor Red
        Write-Host ""
        Write-Host "Common issues:" -ForegroundColor Yellow
        Write-Host "1. GitHub repository might not be accessible" -ForegroundColor White
        Write-Host "2. app.yaml might have errors" -ForegroundColor White
        Write-Host "3. Need to authorize DigitalOcean to access GitHub" -ForegroundColor White
        Write-Host ""
        Write-Host "Try deploying via Web UI instead:" -ForegroundColor Yellow
        Write-Host "  https://cloud.digitalocean.com/apps/new" -ForegroundColor White
        Write-Host ""
    }
} catch {
    Write-Host "❌ Error during deployment!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "📚 Full documentation: DEPLOY_NOW.md" -ForegroundColor Cyan
Write-Host ""
