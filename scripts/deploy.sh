#!/bin/bash
# Deployment script

set -e

echo "Deploying Web Agent Platform..."

# Build Docker image
echo "Building Docker image..."
docker build -t web-agent-platform:latest .

# Run with docker-compose
echo "Starting services..."
docker-compose up -d

echo "Deployment complete!"
echo "API available at http://localhost:8000"
