# Hetzner VPS Setup Guide

Follow these steps to prepare your fresh Hetzner VPS for the Glitch Text Generator.

## 0. DNS Configuration
Before configuring the server, point your domain to the VPS IP address:

1. Log in to your domain registrar (Cloudflare, Namecheap, etc.).
2. Go to **DNS Settings**.
3. Add an **A Record**:
   - **Name**: `@` (or your domain)
   - **Value**: `YOUR_VPS_IP_ADDRESS`
4. Add another **A Record** (or CNAME) for `www`:
   - **Name**: `www`
   - **Value**: `YOUR_VPS_IP_ADDRESS`

*Note: DNS changes can take a few minutes to several hours to propagate.*

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
# Install Docker (if not already installed)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Create project-specific directory
mkdir -p ~/glitch-text-generator
```

## 3. Install Nginx & Certbot (if not already installed)
```bash
apt install nginx certbot python3-certbot-nginx -y
```

## 4. Configure Nginx for Multi-Project Hosting
Nginx handles multiple projects using "Server Blocks". You can have many config files in `sites-available`.

Create a new Nginx config file for *this* project:
```bash
nano /etc/nginx/sites-available/glitch-text
```

Paste the following (replace `yourdomain.com` with your actual domain). 

**Note on Ports:** If port `8000` is already taken by another project on your VPS, change the `8000` in both `docker-compose.yml` and this Nginx config to something else (like `8001`).

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

Enable the new site and restart Nginx:
```bash
ln -s /etc/nginx/sites-available/glitch-text /etc/nginx/sites-enabled/
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
