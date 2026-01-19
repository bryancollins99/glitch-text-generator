# VPS Multi-Project Deployment Guide

This guide documents how to deploy additional projects to this Hetzner VPS. Keep this file on the server at `/root/VPS_MULTI_PROJECT_GUIDE.md` for easy reference.

## Current Server Setup

| Project | Domain | Port | Directory |
|---------|--------|------|-----------|
| Glitch Text Generator | glitchtexteffect.com | 8000 | ~/glitch-text-generator |
| Plausible Analytics | stats.bryancollins.com | 8001 | (existing setup) |

**Next available port: 8002**

---

## Adding a New Project

### Step 1: Choose a Port
Pick the next available port from the table above. Update the table after deploying.

### Step 2: Create Project Directory
```bash
mkdir -p ~/your-project-name
cd ~/your-project-name
```

### Step 3: Create docker-compose.yml
```yaml
services:
  your-project-name:
    image: ghcr.io/yourusername/your-project:latest
    container_name: your-project-name
    restart: always
    ports:
      - "8002:8000"  # Change 8002 to your chosen port
    environment:
      - NODE_ENV=production
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Step 4: Create Nginx Config
```bash
nano /etc/nginx/sites-available/your-project
```

Paste this template (replace values in ALL CAPS):
```nginx
server {
    server_name YOUR_DOMAIN.COM;

    location / {
        proxy_pass http://localhost:YOUR_PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 5: Enable the Site
```bash
ln -s /etc/nginx/sites-available/your-project /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 6: Get SSL Certificate
```bash
certbot --nginx -d YOUR_DOMAIN.COM
```
Choose option 2 (Redirect) when prompted.

### Step 7: Start the Container
```bash
cd ~/your-project-name
docker compose up -d
```

---

## Useful Commands

### Check Running Containers
```bash
docker ps
```

### View Logs for a Project
```bash
docker logs -f container-name
```

### Restart a Project
```bash
cd ~/project-directory
docker compose restart
```

### Check Which Ports Are in Use
```bash
ss -tulpn | grep LISTEN
```

### List All Nginx Sites
```bash
ls -la /etc/nginx/sites-enabled/
```

### Test Nginx Config
```bash
nginx -t
```

### Renew All SSL Certificates
```bash
certbot renew --dry-run
```

---

## Troubleshooting

### 502 Bad Gateway
- Container not running: `docker ps` to check
- Wrong port in Nginx config
- Container crashed: `docker logs container-name`

### SSL Certificate Error
- DNS not propagated yet (wait 5-10 min)
- Forgot to run `certbot --nginx -d domain.com`
- Wrong `server_name` in Nginx config

### Port Already in Use
- Check what's using it: `ss -tulpn | grep :PORT`
- Choose a different port

### Nginx Won't Restart
- Check config syntax: `nginx -t`
- Look for duplicate `server_name` entries
- Check error log: `tail -20 /var/log/nginx/error.log`

---

## GitHub Actions Setup (for auto-deploy)

For each new project, add these secrets to the GitHub repo:
- `VPS_HOST`: 157.180.69.72
- `VPS_SSH_KEY`: (your private SSH key)

---

## Security Notes

1. **Don't use root for deployments** - Consider creating a `deploy` user
2. **Use project-specific SSH keys** - Easier to revoke if compromised
3. **Keep Docker images updated** - Run `docker compose pull` periodically
4. **Monitor disk space** - `df -h` to check

---

*Last updated: January 2026*
