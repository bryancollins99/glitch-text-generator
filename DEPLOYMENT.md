# Deployment Guide for Glitch Text Generator

This document provides detailed instructions for deploying the Glitch Text Generator application to a DigitalOcean droplet using Docker and Nginx.

## Deployment Architecture

The application uses the following architecture:
- **Web Server**: Nginx (reverse proxy)
- **Application Server**: Gunicorn (WSGI server)
- **Container**: Docker
- **Platform**: DigitalOcean Droplet
- **Domain**: glitchtexteffect.com

## Prerequisites

- A DigitalOcean account
- A domain name pointed to your DigitalOcean droplet
- SSH access to your droplet
- Docker installed on your local machine (optional)

## Initial Server Setup

### 1. Create a DigitalOcean Droplet

1. Log in to your DigitalOcean account
2. Create a new Droplet with Ubuntu 22.04 LTS
3. Choose a plan with at least 1GB RAM
4. Select a datacenter region close to your target audience
5. Add your SSH key for secure access

### 2. Configure DNS

1. Add an A record in your domain's DNS settings:
   - Host: @ (or subdomain)
   - Points to: Your droplet's IP address
   - TTL: 3600 (or automatic)

### 3. Initial Server Configuration

SSH into your server and set up the basic environment:

```bash
# Update system packages
apt-get update && apt-get upgrade -y

# Install Docker
apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce

# Install Nginx
apt-get install -y nginx

# Enable and start services
systemctl enable docker
systemctl start docker
systemctl enable nginx
systemctl start nginx
```

## Deployment Process

### 1. SSH Key Setup

On your local machine, ensure you have an SSH key for the server:

```bash
# Generate a key if needed
ssh-keygen -t rsa -b 4096 -f ~/.ssh/do_server_key

# Copy the key to the server
ssh-copy-id -i ~/.ssh/do_server_key root@YOUR_DROPLET_IP
```

### 2. Configure SSH

Create or edit `~/.ssh/config` to include:

```
Host glitch-server
  HostName 64.23.179.161
  User root
  IdentityFile ~/.ssh/do_server_key
```

### 3. Automated Deployment

The project includes a `deploy.sh` script that handles the deployment process:

```bash
# Run the deployment script
cd /path/to/glitch_text_generator
bash deploy.sh
```

The script performs the following actions:
- Commits and pushes changes to GitHub
- Pulls the latest code on the server
- Builds a Docker container
- Starts the container with the right configuration
- Sets up Nginx as a reverse proxy
- Configures SSL with Let's Encrypt (if needed)

### 4. Manual Deployment

If you need to deploy manually, follow these steps:

```bash
# SSH into your server
ssh -i ~/.ssh/do_server_key root@64.23.179.161

# Navigate to the application directory
cd /var/www/glitch-text-generator

# Pull the latest code
git pull

# Build the Docker image
docker build -t glitch-text-generator .

# Stop and remove the existing container
docker stop glitch-app || true
docker rm glitch-app || true

# Start a new container
docker run -d --restart unless-stopped --name glitch-app -p 8000:8000 -e FLASK_APP=app.py -e FLASK_ENV=production glitch-text-generator
```

## Nginx Configuration

The Nginx configuration is created automatically by the deployment script. Here's the configuration:

```nginx
server {
    listen 80;
    server_name glitchtexteffect.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

## SSL Configuration

To enable HTTPS with Let's Encrypt:

```bash
# Install Certbot
apt-get update
apt-get install -y certbot python3-certbot-nginx

# Obtain and install certificate
certbot --nginx -d glitchtexteffect.com --non-interactive --agree-tos --email your-email@example.com
```

## Maintenance

### Server Updates

Regularly update your server to maintain security:

```bash
apt-get update && apt-get upgrade -y
```

### Monitoring Logs

View application logs:

```bash
docker logs glitch-app
```

### Backup

Backup your application code and configuration:

```bash
# On your local machine
rsync -avz -e "ssh -i ~/.ssh/do_server_key" root@64.23.179.161:/var/www/glitch-text-generator /path/to/backup
```

## Troubleshooting

### Application Not Responding

Check if the container is running:

```bash
docker ps | grep glitch-app
```

If not running, check the logs:

```bash
docker logs glitch-app
```

### Nginx Issues

Check Nginx status:

```bash
systemctl status nginx
```

Test Nginx configuration:

```bash
nginx -t
```

### SSL Certificate Issues

Renew certificates:

```bash
certbot renew
```

## SEO Pages Update

If you need to add or modify SEO pages:

1. Edit the `seo_routes.py` file on the server:
   ```bash
   nano /var/www/glitch-text-generator/seo_routes.py
   ```

2. Add new routes following the existing pattern:
   ```python
   @seo_blueprint.route('/new-keyword')
   def new_keyword():
       return render_template('index.html', 
                            title='New Keyword - Custom Title',
                            meta_description='Custom meta description for SEO.',
                            h1_title='New Keyword Generator')
   ```

3. Rebuild and restart the Docker container:
   ```bash
   cd /var/www/glitch-text-generator
   docker stop glitch-app
   docker rm glitch-app
   docker build -t glitch-text-generator .
   docker run -d --restart unless-stopped --name glitch-app -p 8000:8000 -e FLASK_APP=app.py -e FLASK_ENV=production glitch-text-generator
   ```
