#!/bin/bash

# AI-Powered Terminal - Full Stack Startup Script

echo "========================================="
echo "🚀 Starting AI Terminal Full Stack"
echo "========================================="
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi
echo "✅ Python 3 found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi
echo "✅ Node.js found"

# Check if mini-bash exists
if [ ! -f "$SCRIPT_DIR/mini-bash" ]; then
    echo "⚠️  mini-bash not found. Building..."
    cd "$SCRIPT_DIR"
    make clean && make
    echo "✅ mini-bash built"
fi

echo ""
echo "========================================="
echo "🔧 Setting up Backend..."
echo "========================================="

cd "$SCRIPT_DIR/backend"

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install dependencies
source venv/bin/activate
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installing Python dependencies..."
    pip install -q -r requirements.txt
    touch venv/.installed
fi

# Check .env
if [ ! -f ".env" ]; then
    echo "📝 Creating backend/.env..."
    cp .env.example .env
    echo "⚠️  Please add your GEMINI_API_KEY to backend/.env"
fi

echo ""
echo "========================================="
echo "🎨 Setting up Frontend..."
echo "========================================="

cd "$SCRIPT_DIR/frontend"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📥 Installing Node dependencies (this may take a minute)..."
    npm install
fi

# Create .env if needed
if [ ! -f ".env" ]; then
    echo "📝 Creating frontend/.env..."
    cp .env.example .env
fi

echo ""
echo "========================================="
echo "🚀 Starting Servers..."
echo "========================================="
echo ""

# Start backend
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
python app.py > "$SCRIPT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   📍 http://localhost:5000"
echo "   📄 Logs: backend.log"

# Wait for backend to start
sleep 3

# Start frontend
cd "$SCRIPT_DIR/frontend"
npm start > "$SCRIPT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "   📍 http://localhost:3000"
echo "   📄 Logs: frontend.log"

echo ""
echo "========================================="
echo "🎉 AI Terminal is Running!"
echo "========================================="
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend:  http://localhost:5000"
echo ""
echo "📝 Press Ctrl+C to stop all servers"
echo "========================================="
echo ""

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID

