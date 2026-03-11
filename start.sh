#!/bin/bash
# Startup script for Render deployment
# This ensures database is initialized before starting the app

echo "🚀 Starting ASD Detection System..."

# Check if using PostgreSQL or SQLite
if [ -n "$DATABASE_URL" ]; then
    echo "✅ Using PostgreSQL database (production)"
    echo "📊 Database will be auto-initialized on first connection"
else
    echo "📁 Using SQLite database"
    # Initialize SQLite database if it doesn't exist
    if [ ! -f "asd_database.db" ]; then
        echo "🔧 Initializing new SQLite database..."
        python init_database.py
    else
        echo "✅ Database file exists"
    fi
fi

# Start the application with Gunicorn
echo "🌐 Starting web server..."
exec gunicorn app:app
