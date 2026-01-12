# Hetzner VPS Setup Guide

Follow these steps to prepare your fresh Hetzner VPS for the Glitch Text Generator.

## 1. Initial Server Prep
Connect to your VPS via SSH:
```bash
ssh root@your_vps_ip
```

Update system packages:
```bash
apt update && apt upgrade -y
```

## 2. Install Docker & Docker Compose
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Create app directory
mkdir -p ~/app
```

## 3. Install Nginx & Certbot
```bash
apt install nginx certbot python3-certbot-nginx -y
```

## 4. Configure Nginx
Create a new Nginx config file:
```bash
nano /etc/nginx/sites-available/glitch-text
```

Paste the following (replace `yourdomain.com` with your actual domain):
```nginx
server {
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site and restart Nginx:
```bash
ln -s /etc/nginx/sites-available/glitch-text /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

## 5. Get SSL Certificate
```bash
certbot --nginx -d yourdomain.com
```

## 6. GitHub Repository Secrets
Add these to your GitHub repo settings (**Settings > Secrets and variables > Actions**):

- `VPS_HOST`: Your VPS IP address.
- `VPS_SSH_KEY`: The **private** SSH key used to connect to the server (ensure the public key is in `~/.ssh/authorized_keys` on the VPS).
- `GITHUB_TOKEN`: This is automatically provided by GitHub Actions, but the workflow needs `packages: write` permission (already included in the YAML).

## 7. First Deployment
Once secrets are added, push to the `main` branch to trigger the first deployment.
