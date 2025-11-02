#!/bin/bash

# Manus Agent - Quick Start Script for Local Development

echo "🚀 Manus Agent System - Quick Start"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your API keys:"
    echo "   - OPENAI_API_KEY or ANTHROPIC_API_KEY (required)"
    echo "   - NEWS_API_KEY (optional but recommended)"
    echo "   - DATABASE_URL (if using external database)"
    echo ""
    read -p "Press Enter after you've configured .env file..."
fi

# Check if PostgreSQL is needed
read -p "Do you have PostgreSQL installed locally? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⚠️  PostgreSQL is required. Install it:"
    echo "   - macOS: brew install postgresql"
    echo "   - Ubuntu: sudo apt-get install postgresql"
    echo "   - Windows: Download from postgresql.org"
    echo ""
    echo "Then create database: createdb manus_agent"
    exit 1
fi

# Check if Redis is needed
read -p "Do you have Redis installed locally? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⚠️  Redis is required. Install it:"
    echo "   - macOS: brew install redis"
    echo "   - Ubuntu: sudo apt-get install redis-server"
    echo "   - Windows: Download from redis.io"
    echo ""
    echo "Then start Redis: redis-server"
    exit 1
fi

# Initialize database
echo "🗄️  Initializing database..."
python scripts/init_system.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Start Redis: redis-server (in another terminal)"
echo "   2. Start API: uvicorn app.main:app --reload"
echo "   3. Start Worker: celery -A app.workers.celery_app worker --loglevel=info (in another terminal)"
echo "   4. Visit: http://localhost:8000/docs"
echo ""
echo "📚 For deployment, see DEPLOYMENT_GUIDE.md"
echo ""
