#!/bin/bash

# AI-Powered Terminal - Frontend Startup Script

echo "========================================="
echo "🎨 Starting AI Terminal Frontend..."
echo "========================================="

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

# Start the frontend server
echo ""
echo "========================================="
echo "🌐 Frontend starting on http://localhost:3000"
echo "========================================="
echo "Will open automatically in your browser..."
echo ""

npm start

