#!/bin/bash

# Advanced Mini Bash - Voice Control Setup Script (Phase 3)
# This script sets up the voice-controlled shell with Google Cloud APIs

echo "🔥 Advanced Mini Bash - Voice Control Setup (Phase 3)"
echo "======================================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
print_status "Checking Python 3 installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    print_status "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION found"

# Check if pip is installed
print_status "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed!"
    print_status "Please install pip3"
    exit 1
fi

print_success "pip3 found"

# Create virtual environment
print_status "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip
print_success "pip upgraded"

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Check for audio system dependencies
print_status "Checking audio system dependencies..."

# Check for PortAudio (required by pyaudio)
if ! pkg-config --exists portaudio-2.0; then
    print_warning "PortAudio not found. Installing..."
    
    # Detect OS and install accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install portaudio
        else
            print_error "Homebrew not found. Please install PortAudio manually"
            print_status "Run: brew install portaudio"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y portaudio19-dev python3-pyaudio
        elif command -v yum &> /dev/null; then
            sudo yum install -y portaudio-devel python3-pyaudio
        else
            print_warning "Package manager not detected. Please install PortAudio manually"
        fi
    else
        print_warning "OS not detected. Please install PortAudio manually"
    fi
else
    print_success "PortAudio found"
fi

# Build Mini Bash if not exists
print_status "Building Mini Bash shell..."
if [ ! -f "./mini-bash" ]; then
    make clean && make
    if [ $? -eq 0 ]; then
        print_success "Mini Bash built successfully"
    else
        print_error "Failed to build Mini Bash"
        exit 1
    fi
else
    print_success "Mini Bash already exists"
fi

# Create Google Cloud credentials template
print_status "Setting up Google Cloud credentials..."
if [ ! -f "credentials.json" ]; then
    cat > credentials_template.json << EOF
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
EOF
    print_warning "Google Cloud credentials template created"
    print_status "Please replace 'credentials_template.json' with your actual credentials.json"
    print_status "Get credentials from: https://console.cloud.google.com/apis/credentials"
else
    print_success "Google Cloud credentials found"
fi

# Create test script
print_status "Creating test script..."
cat > test_voice.py << 'EOF'
#!/usr/bin/env python3
"""Test script for voice control module"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from voice_module import VoiceControlledShell
    
    print("🎤 Testing Voice Control Module...")
    print("This is a quick test to verify everything is working.")
    print("Press Ctrl+C to exit the test.")
    
    # Test initialization
    voice_shell = VoiceControlledShell()
    print("✅ Voice control module initialized successfully!")
    print("✅ All dependencies loaded correctly!")
    print("✅ Ready to use voice commands!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please check your dependencies installation.")
except Exception as e:
    print(f"❌ Error: {e}")
EOF

chmod +x test_voice.py
print_success "Test script created"

# Create usage examples
print_status "Creating usage examples..."
cat > voice_examples.md << 'EOF'
# Voice Control Examples

## Hindi Commands (हिंदी)
- "फोल्डर खोलो" → `ls`
- "वर्तमान फोल्डर" → `pwd`
- "ऊपर जाओ" → `cd ..`
- "फाइल बनाओ" → `touch newfile.txt`
- "सिस्टम जानकारी" → `uname -a`
- "गिट स्टेटस" → `git status`
- "बाहर निकलो" → `exit`

## English Commands
- "list files" → `ls`
- "current directory" → `pwd`
- "go up" → `cd ..`
- "create file" → `touch newfile.txt`
- "system info" → `uname -a`
- "git status" → `git status`
- "exit" → `exit`

## How to Use
1. Run: `python3 voice_module.py`
2. Wait for "Listening..." prompt
3. Speak your command clearly
4. The shell will execute the command automatically
5. Say "exit" or "बाहर निकलो" to quit
EOF

print_success "Usage examples created"

# Final instructions
echo
echo "🎉 Setup Complete!"
echo "=================="
echo
print_success "Voice-controlled Mini Bash is ready!"
echo
print_status "Next steps:"
echo "1. Place your Google Cloud credentials.json file in this directory"
echo "2. Run: python3 voice_module.py"
echo "3. Start speaking your commands!"
echo
print_status "Test the setup:"
echo "python3 test_voice.py"
echo
print_status "For more examples, see: voice_examples.md"
echo
print_success "Happy voice controlling! 🎤🔥"
