#!/bin/bash

# AI-Powered Terminal - Backend Startup Script

echo "========================================="
echo "🚀 Starting AI Terminal Backend..."
echo "========================================="

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
    echo "✅ Dependencies installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Creating .env from example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit backend/.env and add your GEMINI_API_KEY"
    echo "Get your key from: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter to continue (make sure to add API key first)..."
fi

# Check if mini-bash exists
if [ ! -f "../mini-bash" ]; then
    echo "⚠️  mini-bash not found. Building..."
    cd ..
    make clean && make
    cd backend
    echo "✅ mini-bash built successfully"
fi

# Start the backend server
echo ""
echo "========================================="
echo "🌐 Backend starting on http://localhost:5000"
echo "========================================="
echo ""

python app.py

