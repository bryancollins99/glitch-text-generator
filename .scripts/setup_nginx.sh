#!/bin/bash
set -e

# This script is intended to be run from the root of the checked-out repository on the server.
# It requires the domain name as the first argument.

if [ -z "$1" ]; then
  echo "Usage: $0 <domain_name>"
  exit 1
fi

DOMAIN="$1"
NGINX_CONF_FILE="/etc/nginx/sites-available/glitch-text-generator"
NGINX_ENABLED_SITE_LINK="/etc/nginx/sites-enabled/glitch-text-generator"

echo "🔧 Checking Nginx configuration for $DOMAIN..."

# Nginx configuration content
# Using a temporary file for the config content to avoid complex quoting with sudo tee
CONFIG_CONTENT=$(cat <<EOF_NGINX_CONFIG
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Optional: If you plan to use Let's Encrypt for SSL (Certbot will modify this)
    # location ~ /.well-known/acme-challenge/ {
    #     allow all;
    #     root /var/www/html; # Or a directory Certbot can write to
    # }
}
EOF_NGINX_CONFIG
)

if [ ! -f "$NGINX_CONF_FILE" ]; then
  echo "Creating Nginx configuration file: $NGINX_CONF_FILE..."
  echo "$CONFIG_CONTENT" | sudo tee "$NGINX_CONF_FILE" > /dev/null
  echo "Nginx configuration file created."
else
  echo "Nginx configuration file $NGINX_CONF_FILE already exists."
  # Optionally, overwrite if you always want the latest version from the script:
  # echo "Overwriting existing Nginx configuration file: $NGINX_CONF_FILE..."
  # echo "$CONFIG_CONTENT" | sudo tee "$NGINX_CONF_FILE" > /dev/null
fi

if [ ! -L "$NGINX_ENABLED_SITE_LINK" ]; then
  echo "Enabling Nginx site..."
  sudo ln -sf "$NGINX_CONF_FILE" "$NGINX_ENABLED_SITE_LINK"
else
  echo "Nginx site already enabled."
fi

echo "Testing Nginx configuration..."
if sudo nginx -t; then
  echo "Nginx configuration test successful."
  echo "Reloading Nginx..."
  sudo systemctl reload nginx
  echo "Nginx reloaded."
else
  echo "❌ Nginx configuration test failed. Please check the Nginx config on the server."
  exit 1
fi

echo "✅ Nginx setup/check complete." 