# Deployment Guide for Glitch Text Generator

This document provides detailed instructions for deploying the Glitch Text Generator application to Render.

## Deployment Architecture

The application uses the following architecture:
- **Platform**: Render (Cloud Platform)
- **Container**: Docker
- **Application Server**: Gunicorn (WSGI server)
- **Auto-deployment**: Git-based deployment from GitHub

## Prerequisites

- A Render account (free tier available)
- GitHub repository with your code
- Domain name (optional - Render provides free subdomain)

## Render Deployment Setup

### 1. Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### 2. Deploy from GitHub

#### Option A: Using Render Dashboard

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository: `bryancollins99/glitch_text_generator`
4. Configure the service:
   - **Name**: `glitch-text-generator`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile`
5. Set environment variables:
   - `FLASK_ENV`: `production`
   - `FLASK_APP`: `app.py`
6. Click "Create Web Service"

#### Option B: Using render.yaml (Infrastructure as Code)

The repository includes a `render.yaml` file that automatically configures the deployment:

```yaml
services:
  - type: web
    name: glitch-text-generator
    env: docker
    repo: https://github.com/bryancollins99/glitch_text_generator.git
    branch: main
    dockerfilePath: ./Dockerfile
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_APP
        value: app.py
    healthCheckPath: /
    autoDeploy: true
```

To use this:
1. In Render dashboard, go to "Blueprint"
2. Click "New Blueprint Instance"
3. Connect your repository
4. Render will automatically read the `render.yaml` and deploy

### 3. Custom Domain Setup (Optional)

1. In your Render service dashboard, go to "Settings"
2. Scroll to "Custom Domains"
3. Add your domain (e.g., `glitchtexteffect.com`)
4. Update your domain's DNS settings:
   - Add a CNAME record pointing to your Render service URL
   - Or add an A record pointing to Render's IP addresses

### 4. SSL Certificate

Render automatically provides SSL certificates for all domains (both custom and Render subdomains).

## Automatic Deployment

### Git-based Deployment

Render automatically deploys when you push to the `main` branch:

1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update application"
   git push origin main
   ```
3. Render automatically detects the changes and redeploys

### Build Process

Render follows this process:
1. Pulls latest code from GitHub
2. Builds Docker image using your Dockerfile
3. Runs the container with Gunicorn
4. Makes the service available on the provided URL

## Environment Configuration

### Environment Variables

Set these in the Render dashboard under "Environment":

- `FLASK_ENV`: `production`
- `FLASK_APP`: `app.py`
- `PORT`: Automatically set by Render

### Application Configuration

The application is configured to work with Render:

- **Port**: Uses `PORT` environment variable (set by Render)
- **Gunicorn**: Configured in `gunicorn_config.py`
- **Docker**: Optimized Dockerfile for Render deployment

## Monitoring and Logs

### Viewing Logs

1. Go to your service in Render dashboard
2. Click on "Logs" tab
3. View real-time application logs

### Health Checks

Render automatically monitors your application:
- Health check endpoint: `/` (homepage)
- Automatic restarts if the service becomes unhealthy

### Metrics

Render provides built-in metrics:
- Response times
- Memory usage
- CPU usage
- Request volume

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check the build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify Dockerfile syntax

2. **Application Won't Start**
   - Check application logs
   - Verify `gunicorn_config.py` settings
   - Ensure `wsgi.py` is correctly configured

3. **Port Issues**
   - Render automatically sets the `PORT` environment variable
   - Application binds to `0.0.0.0:$PORT`

### Getting Help

- Check Render documentation: [render.com/docs](https://render.com/docs)
- View application logs in Render dashboard
- Check GitHub Actions for CI status

## Cost

- **Free Tier**: Available with limitations (sleeps after inactivity)
- **Paid Plans**: Starting at $7/month for always-on services
- **Custom Domains**: Free SSL certificates included

## Migration from DigitalOcean

If migrating from DigitalOcean:

1. The application code remains the same
2. Remove DigitalOcean-specific files (already done):
   - `deploy.sh`
   - SSH deployment scripts
3. Update DNS to point to Render instead of DigitalOcean
4. Cancel DigitalOcean droplet once migration is complete

## Backup and Recovery

- **Code**: Backed up in GitHub repository
- **Database**: Not applicable (stateless application)
- **Configuration**: Stored in `render.yaml` and environment variables

Your application will be available at:
- Render subdomain: `https://glitch-text-generator.onrender.com`
- Custom domain: `https://glitchtexteffect.com` (if configured)
