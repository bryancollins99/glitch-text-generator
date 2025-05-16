#!/bin/bash

echo "🚀 Starting deployment to DigitalOcean..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ git is not installed. Please install git."
    exit 1
fi

# Skip local Docker check since we only need it on the server
echo "ℹ️ Skipping local Docker check - only needed on server"

# Check if SSH key exists
SSH_KEY="/Users/bryancollins/.ssh/do_server_key"
if [ ! -f "${SSH_KEY}" ]; then
    echo "❌ SSH key not found at ${SSH_KEY}. Please ensure your DigitalOcean SSH key is available."
    exit 1
fi

# Configuration - Update these values with your DigitalOcean droplet info
DROPLET_IP="64.23.179.161"  # Your Digital Ocean droplet IP
SSH_USER="root"            # Your SSH user
REMOTE_DIR="/var/www/glitch-text-generator"
DOMAIN="glitchtext.com"    # Update with your actual domain

# Commit changes to git
echo "💾 Committing changes to git..."
git add .
git commit -m "Deployment update $(date)" || true

# Push changes to GitHub
echo "🔄 Pushing changes to GitHub..."
git push origin main || true

# Build and deploy Docker container
echo "📥 Pulling latest changes on server..."
ssh -i $SSH_KEY $SSH_USER@$DROPLET_IP "mkdir -p $REMOTE_DIR && cd $REMOTE_DIR && git pull || git clone https://github.com/bryancollins99/glitch_text_generator.git ."

echo "🚫 Stopping old container..."
ssh -i $SSH_KEY $SSH_USER@$DROPLET_IP "cd $REMOTE_DIR && docker stop glitch-app || true && docker rm glitch-app || true"

echo "🏗️ Building new container..."
ssh -i $SSH_KEY $SSH_USER@$DROPLET_IP "cd $REMOTE_DIR && docker build -t glitch-text-generator ."

echo "▶️ Starting new container..."
ssh -i $SSH_KEY $SSH_USER@$DROPLET_IP "cd $REMOTE_DIR && docker run -d --restart unless-stopped --name glitch-app -p 8000:8000 glitch-text-generator"

# Configure Nginx if needed
echo "🔧 Checking Nginx configuration..."
ssh -i $SSH_KEY $SSH_USER@$DROPLET_IP "if [ ! -f /etc/nginx/sites-available/glitch-text-generator ]; then
  echo 'Creating Nginx configuration...'
  cat > /etc/nginx/sites-available/glitch-text-generator << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \\$host;
        proxy_set_header X-Real-IP \\$remote_addr;
        proxy_set_header X-Forwarded-For \\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\$scheme;
    }
}
EOF
  ln -s /etc/nginx/sites-available/glitch-text-generator /etc/nginx/sites-enabled/ 2>/dev/null || true
  nginx -t && systemctl reload nginx
fi"

echo "✅ Deployment complete!"
echo "   Your app is now available at: http://$DOMAIN or http://$DROPLET_IP:8000"
