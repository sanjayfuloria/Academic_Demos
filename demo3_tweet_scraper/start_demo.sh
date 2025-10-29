#!/bin/bash
# Quick start script for Tweet Scraper Demo

echo "=================================================="
echo "Tweet Scraper - Nonprofit Communication Analysis"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run tests
echo "🧪 Running tests..."
python -m unittest test_tweet_scraper.py -v
echo ""

# Offer to run the demo
echo "=================================================="
echo "Setup complete! Choose an option:"
echo "=================================================="
echo ""
echo "1. Run command-line demo (python tweet_scraper.py)"
echo "2. Launch interactive dashboard (streamlit run app.py)"
echo "3. Exit"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Running command-line demo..."
        echo ""
        python tweet_scraper.py
        ;;
    2)
        echo ""
        echo "🌐 Launching interactive dashboard..."
        echo "📍 Open your browser to http://localhost:8501"
        echo ""
        streamlit run app.py
        ;;
    3)
        echo "👋 Goodbye!"
        ;;
    *)
        echo "Invalid choice. Exiting."
        ;;
esac
