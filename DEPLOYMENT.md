# Git Deployment Guide - Glitch Text Generator

## Overview
This guide covers the deployment process for the Glitch Text Generator application from local development to production environments.

## Prerequisites
- Git installed and configured
- Python 3.9+ installed
- Access to the production hosting environment (Render.com or DigitalOcean)
- Environment variables configured

## Development Workflow

### 1. Local Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd glitch-text-generator

# Install dependencies
pip3 install -r requirements.txt

# Start local development server
PORT=9600 python3 app.py
```

### 2. Feature Development Process
```bash
# Create a new feature branch
git checkout -b feature/your-feature-name

# Make your changes and test locally
# Add and commit changes
git add .
git commit -m "Add: Description of your changes"

# Push feature branch
git push origin feature/your-feature-name
```

## Git Workflow

### Branch Strategy
- `main` - Production branch (stable, deployed code)
- `develop` - Development branch (latest features)
- `feature/*` - Feature branches for new functionality
- `hotfix/*` - Emergency fixes for production

### Commit Convention
Use conventional commit messages:
```
feat: add new glitch text effect
fix: resolve CSS display issue on mobile
docs: update README with new features
style: improve button hover animations
refactor: optimize image processing logic
test: add unit tests for text generation
```

## Pre-Deployment Checklist

### Code Quality Checks
- [ ] All tests pass locally
- [ ] No console errors in browser
- [ ] Mobile responsiveness tested
- [ ] All internal links working
- [ ] SEO meta tags updated
- [ ] CSS/JS minification (if applicable)

### Content Validation
- [ ] All new pages have proper meta descriptions
- [ ] Sitemap updated with new routes
- [ ] Related resources links added between content pages
- [ ] Images optimized and paths correct
- [ ] No broken external links

### Security Review
- [ ] No sensitive data in commit history
- [ ] Environment variables properly configured
- [ ] CSP headers allow necessary external resources
- [ ] HTTPS enforced in production

## Deployment Process

### Step 1: Prepare for Deployment
```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Merge your feature branch
git merge feature/your-feature-name

# Run final tests
python3 -m pytest (if tests exist)
```

### Step 2: Tag Release (Optional)
```bash
# Create a version tag
git tag -a v1.2.3 -m "Release version 1.2.3: Add internal linking"
git push origin v1.2.3
```

### Step 3: Deploy to Production

#### For Render.com Deployment
```bash
# Push to main branch (auto-deploys)
git push origin main

# Monitor deployment in Render dashboard
# Check deployment logs for any issues
```

#### For Manual Server Deployment
```bash
# SSH into production server
ssh user@your-server.com

# Navigate to app directory
cd /path/to/glitch-text-generator

# Pull latest changes
git pull origin main

# Install/update dependencies
pip3 install -r requirements.txt

# Restart the application
sudo systemctl restart glitch-text-generator
# OR using PM2: pm2 restart glitch-text-generator
```

### Step 4: Post-Deployment Verification
1. Visit the live site and test core functionality
2. Check that new features work as expected
3. Verify all internal links function correctly
4. Test on mobile devices
5. Check server logs for any errors

## Environment Configuration

### Environment Variables
Create a `.env` file for local development:
```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=9600
```

### Production Environment Variables
Ensure these are set in your hosting environment:
```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
# Add any other production-specific variables
```

## Rollback Procedure

If deployment issues occur:

### Quick Rollback
```bash
# Revert to previous commit
git revert HEAD
git push origin main
```

### Full Rollback to Previous Tag
```bash
# Find previous stable tag
git tag -l

# Reset to previous tag
git reset --hard v1.2.2
git push origin main --force
```

## Monitoring and Maintenance

### Post-Deployment Monitoring
- Monitor server resources (CPU, memory, disk space)
- Check application logs for errors
- Monitor site performance and loading times
- Verify search engine crawling and indexing

### Regular Maintenance Tasks
- Update dependencies monthly
- Review and update content
- Monitor and fix broken links
- Update sitemap as content grows
- Review and optimize performance

## Troubleshooting Common Issues

### Deployment Fails
1. Check commit history for syntax errors
2. Verify all dependencies in requirements.txt
3. Check server logs for specific error messages
4. Ensure environment variables are properly set

### Site Not Loading After Deployment
1. Check server status and logs
2. Verify DNS settings (if domain changed)
3. Check SSL certificate status
4. Verify application is running on correct port

### CSS/JS Not Loading
1. Check file paths in templates
2. Verify static file serving configuration
3. Clear browser cache
4. Check CSP headers for blocked resources

## Security Best Practices

### Before Each Deployment
- Review code for security vulnerabilities
- Ensure no API keys or passwords in code
- Verify CSP headers are properly configured
- Check that user input is properly sanitized

### Git Security
- Never commit sensitive data
- Use .gitignore for environment files
- Regularly review commit history
- Use signed commits for production releases

## Emergency Procedures

### Site Down Emergency
1. Check server status immediately
2. Review recent commits for breaking changes
3. Implement quick rollback if necessary
4. Notify users via social media if extended downtime

### Security Incident
1. Immediately take site offline if compromised
2. Review server logs for breach indicators
3. Change all passwords and API keys
4. Restore from clean backup
5. Implement additional security measures

## Contact Information

**Development Team:**
- Primary Developer: [Your Name]
- Email: [your-email@domain.com]

**Hosting Provider:**
- Platform: Render.com / DigitalOcean
- Support: [hosting-support-contact]

## Notes

⚠️ **IMPORTANT:** Always request permission before deploying to production. Follow this process:

1. Create a detailed deployment plan
2. Request approval from project owner
3. Schedule deployment during low-traffic hours
4. Have rollback plan ready
5. Monitor closely post-deployment

Remember: "Always ask permission before deployment" - as specified in the project requirements.
