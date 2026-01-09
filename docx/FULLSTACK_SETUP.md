# 🚀 AI-Powered Terminal - Full Stack Setup Guide

## Overview

This is a full-stack application that transforms your bash shell into an AI-powered terminal with natural language processing and voice control capabilities using Google's Gemini AI.

## 🎯 Features

### ✨ Core Features
- **Natural Language Processing**: Convert plain English to terminal commands using Gemini AI
- **Voice Control**: Speak your commands using built-in speech recognition
- **Smart File Search**: Find files anywhere on your system automatically
- **Intelligent Directory Switching**: Navigate to file locations automatically
- **Fallback System**: Seamlessly falls back to Mac terminal for unsupported commands
- **Real-time Updates**: WebSocket-powered live terminal updates
- **Command History**: Track all your commands with AI interpretations
- **Feedback Tracking**: Logs commands not supported by mini-bash

### 🤖 AI Capabilities
- Understands natural language like "show me all python files"
- Finds files across your system: "open adi.c in vscode"
- Smart directory navigation: "go to downloads folder"
- Opens files in specific apps: "open config.json in sublime"

## 📋 Prerequisites

### System Requirements
- macOS or Linux
- Python 3.8+
- Node.js 16+
- GCC compiler
- Make

### API Requirements
- Google Gemini API Key (Free tier available)

## 🛠️ Installation

### Step 1: Build the Mini Bash Shell

```bash
# Navigate to project directory
cd /Users/abhisheksinghrawat/Desktop/bash

# Build the C shell
make clean && make

# Verify it works
./mini-bash
# Type 'exit' to quit
```

### Step 2: Set Up Backend (Python)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get your key from: https://makersuite.google.com/app/apikey
nano .env
# Add: GEMINI_API_KEY=your_actual_api_key_here
```

### Step 3: Set Up Frontend (React)

```bash
# Open a new terminal window
# Navigate to frontend directory
cd /Users/abhisheksinghrawat/Desktop/bash/frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# (Default values should work for local development)
```

## 🚀 Running the Application

### Terminal 1: Start Backend Server

```bash
cd /Users/abhisheksinghrawat/Desktop/bash/backend
source venv/bin/activate
python app.py
```

The backend will start on `http://localhost:5000`

### Terminal 2: Start Frontend Server

```bash
cd /Users/abhisheksinghrawat/Desktop/bash/frontend
npm start
```

The frontend will open automatically at `http://localhost:3000`

## 🎮 Usage Examples

### Natural Language Commands

1. **List Files**
   - Type: "show me all python files"
   - AI converts to: `find . -name '*.py'`

2. **Open Files**
   - Type: "open adi.c in vscode"
   - AI finds the file anywhere on your system
   - Changes to that directory
   - Opens in VS Code

3. **Navigate Directories**
   - Type: "go to downloads folder"
   - AI converts to: `cd ~/Downloads`

4. **System Information**
   - Type: "show me disk space"
   - AI converts to: `df -h`

### Voice Commands

1. Click the 🎤 microphone button
2. Speak your command clearly
3. The system will:
   - Transcribe your speech
   - Send it to Gemini AI
   - Execute the interpreted command
   - Show results in real-time

## 📁 Project Structure

```
bash/
├── backend/                  # Python Flask API
│   ├── app.py               # Main backend server with Gemini integration
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (API keys)
│
├── frontend/                # React web application
│   ├── src/
│   │   ├── App.js          # Main application component
│   │   ├── components/      # React components
│   │   │   ├── Header.js   # Header with status indicators
│   │   │   ├── StatusBar.js # Directory status bar
│   │   │   ├── Terminal.js  # Terminal display
│   │   │   └── InputBar.js  # Command input with voice
│   │   └── services/        # API and WebSocket services
│   │       ├── api.js      # REST API client
│   │       └── websocket.js # WebSocket client
│   ├── public/
│   └── package.json
│
├── mini-bash               # Compiled C shell executable
├── *.c                     # C source files
├── headers/                # C header files
└── Makefile               # Build configuration
```

## 🔧 Configuration

### Backend Configuration (`backend/.env`)

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
FLASK_ENV=development
FLASK_DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

### Frontend Configuration (`frontend/.env`)

```bash
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=http://localhost:5000
```

## 🌐 API Endpoints

### REST API

- `GET /api/health` - Health check and system status
- `GET /api/directory` - Get current working directory
- `POST /api/execute` - Execute a command
- `GET /api/history` - Get command history
- `GET /api/feedback` - Get feedback log (unsupported commands)
- `POST /api/search` - Search for files

### WebSocket Events

- `connect` - Client connects to server
- `connected` - Server acknowledges connection
- `execute_command` - Client sends command
- `command_result` - Server sends execution result
- `command_executed` - Broadcast command execution to all clients

## 🎯 How It Works

### Natural Language Processing Flow

1. **User Input**: User types or speaks a command
2. **Speech Recognition** (if voice): Browser's Web Speech API transcribes audio
3. **Send to Backend**: Command sent to Flask server
4. **Gemini AI Processing**: 
   - Server sends command + context to Gemini API
   - AI analyzes intent and generates appropriate terminal command
   - Returns confidence level and metadata
5. **File Search** (if needed):
   - If command requires a file, search system using `find`
   - Automatically switch to file's directory
6. **Command Execution**:
   - Try mini-bash first
   - Fall back to system terminal if unsupported
   - Track feedback for unsupported commands
7. **Response**: Results sent back to frontend in real-time

### Fallback System

```
User Command
    ↓
Gemini AI (interpret)
    ↓
Execute in mini-bash
    ↓
Success? → Return result
    ↓ No
Execute in system terminal
    ↓
Success? → Return result + Log feedback
    ↓ No
Return error
```

## 🔒 Security Considerations

1. **API Keys**: Never commit `.env` files to git
2. **Command Execution**: Be careful with commands that modify system
3. **CORS**: Configure appropriate CORS origins in production
4. **Input Validation**: The backend validates all inputs
5. **Timeout**: Commands have 30-second timeout to prevent hanging

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check if port 5000 is available
lsof -i :5000
```

### Frontend won't start
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 is available
lsof -i :3000
```

### Gemini API errors
```bash
# Verify API key is set
echo $GEMINI_API_KEY

# Check API key in .env file
cat backend/.env

# Test API key
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY"
```

### Voice input not working
- Make sure you're using Chrome or Edge (Safari has limited support)
- Allow microphone permissions when prompted
- Check browser console for errors

### Mini-bash not found
```bash
# Build the shell
cd /Users/abhisheksinghrawat/Desktop/bash
make clean && make

# Check if executable exists
ls -l mini-bash
```

## 📊 Performance

- **Command Processing**: < 2 seconds (with Gemini AI)
- **File Search**: < 5 seconds (depends on system size)
- **WebSocket Latency**: < 100ms
- **Frontend Load Time**: < 1 second

## 🚀 Production Deployment

### Backend (Python)

```bash
# Use production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app --worker-class eventlet
```

### Frontend (React)

```bash
# Build production bundle
npm run build

# Serve with nginx or similar
# Or deploy to Vercel/Netlify
```

## 🎓 Learning Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [React Documentation](https://react.dev)
- [Flask Documentation](https://flask.palletsprojects.com)
- [WebSocket Documentation](https://socket.io/docs/v4/)

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Built with ❤️ using Gemini AI, React, Flask, and C**

