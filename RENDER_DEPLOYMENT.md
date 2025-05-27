# Quick Render Deployment Guide

## 🚀 Deploy to Render in 5 Minutes

### Step 1: Prepare Your Repository
Your repository is already configured for Render with:
- ✅ `render.yaml` configuration file
- ✅ `Dockerfile` optimized for Render
- ✅ `gunicorn_config.py` with dynamic port binding
- ✅ Updated GitHub Actions (CI only, no deployment)

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 3: Deploy Your Service

#### Option A: Automatic Deployment (Recommended)
1. In Render dashboard, click "New +" → "Blueprint"
2. Click "New Blueprint Instance"
3. Connect your GitHub repository: `bryancollins99/glitch_text_generator`
4. Render will automatically read `render.yaml` and deploy
5. Your app will be available at: `https://glitch-text-generator.onrender.com`

#### Option B: Manual Setup
1. In Render dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `glitch-text-generator`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile`
4. Add environment variables:
   - `FLASK_ENV`: `production`
   - `FLASK_APP`: `app.py`
5. Click "Create Web Service"

### Step 4: Custom Domain (Optional)
1. In your service dashboard, go to "Settings"
2. Scroll to "Custom Domains"
3. Add `glitchtexteffect.com`
4. Update your DNS:
   - Add CNAME record: `glitchtexteffect.com` → `glitch-text-generator.onrender.com`

### Step 5: Monitor Deployment
- Watch the build logs in Render dashboard
- First deployment takes 2-3 minutes
- Subsequent deployments are faster due to Docker layer caching

## 🔧 What Changed from DigitalOcean

### Removed Files
- ❌ `deploy.sh` - No longer needed
- ❌ SSH deployment in GitHub Actions
- ❌ Nginx configuration scripts

### Added/Updated Files
- ✅ `render.yaml` - Render configuration
- ✅ Updated `gunicorn_config.py` - Dynamic port binding
- ✅ Updated `Dockerfile` - Render optimized
- ✅ Updated GitHub Actions - CI only

### Benefits of Render
- 🚀 **Automatic deployments** on git push
- 🔒 **Free SSL certificates** for all domains
- 📊 **Built-in monitoring** and logs
- 💰 **Free tier available** (with sleep after inactivity)
- 🛠️ **No server maintenance** required

## 🐛 Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Dockerfile syntax

### App Won't Start
- Check application logs in Render dashboard
- Verify environment variables are set correctly
- Ensure `wsgi.py` imports correctly

### Domain Issues
- DNS changes can take up to 24 hours to propagate
- Use DNS checker tools to verify CNAME records
- Render provides free SSL certificates automatically

## 💰 Pricing
- **Free Tier**: Good for testing (sleeps after 15 minutes of inactivity)
- **Starter Plan**: $7/month for always-on service
- **Pro Plan**: $25/month for enhanced performance

## 🎉 You're Done!
Your glitch text generator is now running on Render with automatic deployments. Every time you push to the `main` branch, Render will automatically rebuild and deploy your application.

Visit your app at: `https://glitch-text-generator.onrender.com` 