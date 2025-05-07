#!/bin/bash

echo "🚀 Starting deployment to GitHub and Netlify..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ git is not installed. Please install git."
    exit 1
fi

# Use locally installed netlify-cli
NETLIFY_CLI="./node_modules/.bin/netlify"

# Check if netlify-cli is installed locally
if [ ! -f "$NETLIFY_CLI" ]; then
    echo "❌ netlify-cli is not installed locally. Installing it now..."
    npm install netlify-cli --save-dev
    
    # Check if installation was successful
    if [ ! -f "$NETLIFY_CLI" ]; then
        echo "❌ Failed to install netlify-cli. Please try manually with: npm install netlify-cli --save-dev"
        exit 1
    fi
fi

# Check if netlify is authenticated
echo "🔑 Checking Netlify authentication..."
if ! $NETLIFY_CLI status &> /dev/null; then
    echo "❌ Not authenticated with Netlify. Please run '$NETLIFY_CLI login' first."
    $NETLIFY_CLI login
fi

# Create netlify.toml if it doesn't exist
if [ ! -f "netlify.toml" ]; then
    echo "📝 Creating netlify.toml configuration file..."
    cat > netlify.toml << EOF
[build]
  command = "npm run build"
  publish = "dist" # Adjust this based on your build output directory

# Handle SPA routing if needed
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
EOF
    echo "✅ netlify.toml created!"
fi

# Build the project
echo "🏗️ Building project..."
npm run build

# Commit changes to git
echo "💾 Committing changes to git..."
git add .
git commit -m "Deployment update $(date)"

# Push changes to GitHub
echo "🔄 Pushing changes to GitHub..."
git push origin main

# Deploy to Netlify
echo "🚀 Deploying to Netlify..."
$NETLIFY_CLI deploy --prod

echo "✅ Deployment complete!"
echo "   Your site is now available on Netlify."
echo "   You can check the status and get the URL with: netlify open"
