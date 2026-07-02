#!/bin/bash
# Installation script for Web Agent Platform

set -e

echo "Installing Web Agent Platform..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install --with-deps chromium

# Create storage directories
echo "Creating storage directories..."
mkdir -p storage/{html,markdown,cache,outputs,vectors}
mkdir -p logs

# Copy environment file if not exists
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file. Please update with your API keys."
fi

echo "Installation complete!"
echo "Run 'source venv/bin/activate' to activate the environment."
