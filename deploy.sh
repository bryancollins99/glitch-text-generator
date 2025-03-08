#!/bin/bash

echo "🚀 Starting deployment..."

echo "📥 Pulling latest changes from GitHub..."
git pull

echo "🛑 Stopping old container..."
docker stop glitch-app || true
docker rm glitch-app || true

echo "🏗️ Building new container..."
docker build -t glitch-text-generator .

echo "▶️ Starting new container..."
docker run -d --restart unless-stopped --name glitch-app -p 8000:8000 glitch-text-generator

echo "✅ Deployment complete!"
