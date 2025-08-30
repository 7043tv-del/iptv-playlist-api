# 🚂 Deploy IPTV API to Railway via GitHub

## 🎯 Overview

This guide will help you deploy your IPTV Playlist API to Railway using GitHub for free, reliable hosting.

## 📋 Prerequisites

1. **GitHub Account** - Sign up at [github.com](https://github.com)
2. **Railway Account** - Sign up at [railway.app](https://railway.app)
3. **Git** - For version control

## 🚀 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name it: `iptv-playlist-api`
4. Make it **Public** (free hosting)
5. Click "Create repository"

### Step 2: Upload Your Code

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/iptv-playlist-api.git
   cd iptv-playlist-api
   ```

2. **Copy your files:**
   - `iptv_api_production.py` → `iptv_api.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `converted_playlist.m3u`
   - `web_interface.html`
   - `.github/workflows/deploy.yml`

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Initial IPTV API commit"
   git push origin main
   ```

### Step 3: Get Railway Token

1. Go to [railway.app](https://railway.app)
2. Login to your account
3. Go to **Account Settings** → **Tokens**
4. Click **New Token**
5. Name it: `IPTV-API-Deploy`
6. Copy the token (keep it secret!)

### Step 4: Add Railway Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

   **Name:** `RAILWAY_TOKEN`
   **Value:** `[Your Railway Token]`

   **Name:** `RAILWAY_SERVICE`
   **Value:** `[Your Railway Service ID]`

### Step 5: Get Railway Service ID

1. In Railway dashboard, go to your project
2. Click on your service
3. Copy the Service ID from the URL or settings

### Step 6: Deploy

1. **Push any change to trigger deployment:**
   ```bash
   echo "# Updated" >> README.md
   git add README.md
   git commit -m "Trigger deployment"
   git push origin main
   ```

2. **Check deployment status:**
   - Go to **Actions** tab in GitHub
   - Watch the deployment progress

## 🔧 Alternative: Manual Railway Deployment

If GitHub Actions doesn't work, use Railway CLI directly:

### Option 1: Upgrade Railway Plan
1. Go to [railway.com/account/plans](https://railway.com/account/plans)
2. Choose a plan that allows deployments
3. Run: `railway up`

### Option 2: Use Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Create new project
3. Choose "Deploy from GitHub"
4. Connect your repository
5. Railway will auto-deploy

## 📁 Required Files Structure

```
iptv-playlist-api/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── iptv_api.py                 # Main API file (renamed from production)
├── requirements.txt             # Python dependencies
├── Procfile                    # Railway process definition
├── runtime.txt                 # Python version
├── converted_playlist.m3u      # Your playlist file
├── web_interface.html          # Web interface
└── README.md                   # Project documentation
```

## 🌐 After Deployment

Your API will be available at:
- **API Base:** `https://your-project.railway.app`
- **Web Interface:** `https://your-project.railway.app/web_interface.html`
- **Health Check:** `https://your-project.railway.app/api/health`

## 🔄 Auto-Updates

Every time you push to GitHub:
1. GitHub Actions automatically triggers
2. Railway redeploys your API
3. Your API stays up-to-date

## 🆘 Troubleshooting

### Common Issues

1. **Build Fails:**
   - Check requirements.txt
   - Verify Python version in runtime.txt

2. **Deployment Fails:**
   - Check Railway token is correct
   - Verify service ID is correct

3. **API Not Starting:**
   - Check Procfile syntax
   - Verify environment variables

### Get Help

- **GitHub Issues:** Create issue in your repository
- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **Community:** [discord.gg/railway](https://discord.gg/railway)

## 🎉 Benefits

- ✅ **Free Hosting** - GitHub + Railway free tiers
- ✅ **Auto-Deploy** - Push code, get updates
- ✅ **Always Online** - 24/7 availability
- ✅ **HTTPS/SSL** - Secure connections
- ✅ **Global CDN** - Fast worldwide access
- ✅ **Version Control** - Track all changes

## 📝 Next Steps

1. Create GitHub repository
2. Upload your code
3. Set up Railway secrets
4. Deploy automatically
5. Share your live API URL!

---

**Your IPTV API will be permanently online and automatically updated!** 🚀
