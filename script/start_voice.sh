#!/bin/bash

# Advanced Mini Bash Shell - Voice Control Starter Script
# This script activates the virtual environment and starts voice control

echo "🎤 Advanced Mini Bash Shell - Voice Control"
echo "=========================================="
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install google-cloud-speech google-cloud-translate google-cloud-texttospeech
    echo "✅ Virtual environment created and dependencies installed"
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if mini-bash exists
if [ ! -f "./mini-bash" ]; then
    echo "❌ Mini Bash not found! Building..."
    make clean && make
    if [ $? -eq 0 ]; then
        echo "✅ Mini Bash built successfully"
    else
        echo "❌ Failed to build Mini Bash"
        exit 1
    fi
else
    echo "✅ Mini Bash found"
fi

# Check for credentials
if [ ! -f "credentials.json" ]; then
    echo "⚠️  Google Cloud credentials not found!"
    echo
    echo "To use voice control, you need Google Cloud API credentials:"
    echo "1. Go to: https://console.cloud.google.com/"
    echo "2. Create a project or select existing"
    echo "3. Enable APIs: Speech-to-Text, Translation, Text-to-Speech"
    echo "4. Create service account and download JSON key"
    echo "5. Rename to 'credentials.json' and place in this directory"
    echo
    echo "For now, starting basic shell without voice control..."
    echo
    ./mini-bash
    exit 0
fi

echo "✅ Google Cloud credentials found"
echo "🎤 Starting voice-controlled shell..."
echo

# Start voice control
python3 voice_enhanced.py
