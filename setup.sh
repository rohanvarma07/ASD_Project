#!/bin/bash

# ========================================
# ASD Detection System - Quick Start Script
# ========================================

echo "=========================================="
echo "ASD DETECTION SYSTEM - SETUP"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "✓ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the app: python app.py"
echo "3. Open browser: http://localhost:5000"
echo ""
echo "Test credentials:"
echo "Email: admin@example.com"
echo "Password: admin123"
echo ""
echo "=========================================="
