#!/bin/bash
# Run script for Web Agent Platform

set -e

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Default values
HOST=${API_HOST:-"0.0.0.0"}
PORT=${API_PORT:-8000}

echo "Starting Web Agent Platform API on $HOST:$PORT..."

# Run with uvicorn
uvicorn api.server:app --host $HOST --port $PORT --reload
