#!/bin/bash
# Database migration script

set -e

echo "Running database migrations..."

# Load environment
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Initialize SQLite schema
echo "Initializing SQLite database..."
python3 -c "import asyncio; from database.sqlite import SQLiteDB; asyncio.run(SQLiteDB().init_schema())"

echo "Migrations complete!"
