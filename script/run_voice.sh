#!/bin/bash

# Advanced Mini Bash Shell - Voice Control Launcher
# This script starts the voice-controlled shell

clear

echo "🔥 Advanced Mini Bash Shell - Voice Control"
echo "==========================================="
echo

# Check credentials
if [ ! -f "credentials.json" ]; then
    echo "❌ credentials.json not found!"
    echo "Please add your Google Cloud credentials first."
    echo "See GET_CREDENTIALS.md for instructions."
    exit 1
fi

echo "✅ credentials.json found"

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check mini-bash
if [ ! -f "./mini-bash" ]; then
    echo "⚠️  Mini Bash not found. Building..."
    make clean && make
fi

echo "✅ All dependencies ready"
echo
echo "🎤 Starting Voice-Controlled Shell..."
echo "==========================================="
echo
echo "📝 How to use:"
echo "   - Wait for 'Listening...' prompt"
echo "   - Speak clearly into your microphone"
echo "   - Say commands in Hindi or English"
echo "   - Say 'exit' or 'बाहर निकलो' to quit"
echo
echo "🎯 Example commands:"
echo "   Hindi:   'फोल्डर खोलो' → ls"
echo "   Hindi:   'वर्तमान फोल्डर' → pwd"
echo "   English: 'list files' → ls"
echo "   English: 'current directory' → pwd"
echo
echo "Press Ctrl+C to stop voice control anytime"
echo "==========================================="
echo

# Set Google Cloud credentials environment variable
export GOOGLE_APPLICATION_CREDENTIALS="credentials.json"

# Start voice control
python3 voice_enhanced.py
