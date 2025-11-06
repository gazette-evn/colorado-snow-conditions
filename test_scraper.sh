#!/bin/bash
# Quick test script for the Colorado Ski scraper

echo "=================================="
echo "Testing Colorado Ski Scraper"
echo "=================================="

# Check if Chrome is installed
if command -v google-chrome &> /dev/null; then
    echo "✅ Chrome is installed"
    google-chrome --version
else
    echo "❌ Chrome not found - install it first"
    echo "  macOS: brew install --cask google-chrome"
    echo "  Ubuntu: see install instructions in workflow"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  No virtual environment found"
fi

# Install/upgrade dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the scraper
echo ""
echo "Running scraper..."
python colorado_ski_scraper.py

# Check if output file was created
if [ -f "colorado_resorts_scraped.csv" ]; then
    echo ""
    echo "✅ SUCCESS! Data scraped to colorado_resorts_scraped.csv"
    echo ""
    echo "Preview:"
    head -10 colorado_resorts_scraped.csv
    echo ""
    wc -l colorado_resorts_scraped.csv
else
    echo ""
    echo "❌ No output file created - check colorado_scraper.log for errors"
    exit 1
fi

