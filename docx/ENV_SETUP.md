# 🔧 Environment Variables Setup Guide

## 📁 Environment Files Created

### Frontend: `frontend/.env`
```bash
# Backend API Configuration
REACT_APP_API_URL=http://localhost:5002
REACT_APP_WS_URL=http://localhost:5002

# App Configuration
REACT_APP_NAME=AI Terminal
REACT_APP_VERSION=1.0.0

# Feature Flags
REACT_APP_ENABLE_VOICE=true
REACT_APP_ENABLE_WEBSOCKET=true
REACT_APP_DEBUG=false
```

### Backend: `backend/.env`
```bash
# Gemini AI Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=

# Flask Server Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=app.py

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# Server Configuration
HOST=0.0.0.0
PORT=5002

# Feature Flags
ENABLE_WEBSOCKET=true
ENABLE_FILE_SEARCH=true
ENABLE_FALLBACK=true
```

## 🔌 How Environment Variables Are Used

### Frontend (React)

#### 1. **API URL** - `REACT_APP_API_URL`
Used in: `src/services/api.js`
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5002';
```
**Purpose:** Base URL for all REST API calls to backend

#### 2. **WebSocket URL** - `REACT_APP_WS_URL`
Used in: `src/services/websocket.js`
```javascript
const WS_URL = process.env.REACT_APP_WS_URL || 'http://localhost:5002';
```
**Purpose:** WebSocket connection endpoint for real-time updates

#### 3. **App Configuration**
- `REACT_APP_NAME`: Application display name
- `REACT_APP_VERSION`: Version number for tracking
- `REACT_APP_ENABLE_VOICE`: Enable/disable voice input feature
- `REACT_APP_ENABLE_WEBSOCKET`: Enable/disable WebSocket connections
- `REACT_APP_DEBUG`: Enable debug logging in browser console

### Backend (Flask)

#### 1. **Gemini API Key** - `GEMINI_API_KEY`
Used in: `backend/app.py`
```python
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
```
**Purpose:** Authenticate with Google Gemini AI for natural language processing

#### 2. **Server Configuration**
- `HOST`: Server bind address (0.0.0.0 = all interfaces)
- `PORT`: Server port number (5002)
- `FLASK_ENV`: development/production mode
- `FLASK_DEBUG`: Enable debug mode with auto-reload

#### 3. **CORS** - `CORS_ORIGINS`
**Purpose:** Allow frontend (localhost:3000) to make API requests

#### 4. **Feature Flags**
- `ENABLE_WEBSOCKET`: Enable WebSocket support
- `ENABLE_FILE_SEARCH`: Enable system-wide file search
- `ENABLE_FALLBACK`: Enable fallback to system terminal

## 🚀 How Integration Works

```
Frontend (React on :3000)
    │
    ├─ REST API Calls ────> REACT_APP_API_URL (:5002)
    │                            │
    │                            ▼
    │                       Backend Flask
    │                            │
    │                            ├─ Gemini AI (GEMINI_API_KEY)
    │                            ├─ Mini-Bash
    │                            └─ System Terminal
    │
    └─ WebSocket ────────> REACT_APP_WS_URL (:5002)
                                 │
                                 ▼
                            Real-time Updates
```

## 🔑 Adding Your Gemini API Key

### Step 1: Get API Key
```bash
# Visit in browser:
open https://makersuite.google.com/app/apikey
```

### Step 2: Add to Backend
```bash
# Edit backend/.env
nano backend/.env

# Add your key (replace with actual key):
GEMINI_API_KEY=AIzaSyD...your_actual_key_here
```

### Step 3: Restart Backend
```bash
# Kill current backend
pkill -f "python app.py"

# Restart with new API key
cd backend
source venv/bin/activate
python app.py &
```

## 🧪 Testing Environment Variables

### Test Frontend Environment
```bash
# Frontend should read from .env automatically
cd frontend
npm start
# Check browser console for loaded env vars
```

### Test Backend Environment
```bash
cd backend
source venv/bin/activate
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('GEMINI_API_KEY:', 'Set' if os.getenv('GEMINI_API_KEY') else 'Not Set')
print('PORT:', os.getenv('PORT', '5002'))
print('FLASK_DEBUG:', os.getenv('FLASK_DEBUG', 'True'))
"
```

## 📝 Environment Variable Rules

### Frontend (React)
- ✅ **MUST** start with `REACT_APP_` prefix
- ✅ Available in code as `process.env.REACT_APP_*`
- ✅ Embedded at **build time** (not runtime)
- ✅ Requires restart of `npm start` to pick up changes

### Backend (Flask)
- ✅ Loaded via `python-dotenv` (optional)
- ✅ Available as `os.getenv('VAR_NAME')`
- ✅ Can be changed at runtime
- ✅ Requires restart of Flask app to pick up changes

## 🔒 Security Best Practices

### ✅ DO:
- Keep `.env` files out of git (already in `.gitignore`)
- Use `.env.example` for documentation
- Rotate API keys regularly
- Use different keys for dev/prod

### ❌ DON'T:
- Commit `.env` files to git
- Share API keys publicly
- Use production keys in development
- Hardcode sensitive values in code

## 🌍 Different Environments

### Development (Current Setup)
```bash
# Frontend
REACT_APP_API_URL=http://localhost:5002

# Backend
FLASK_ENV=development
FLASK_DEBUG=True
```

### Production (Example)
```bash
# Frontend
REACT_APP_API_URL=https://api.yourapp.com

# Backend
FLASK_ENV=production
FLASK_DEBUG=False
GEMINI_API_KEY=<production_key>
```

## 🔄 Restart Services After Changes

### Restart Frontend
```bash
# Kill current
pkill -f "react-scripts"

# Start fresh
cd frontend
npm start
```

### Restart Backend
```bash
# Kill current
pkill -f "python app.py"

# Start fresh
cd backend
source venv/bin/activate
python app.py &
```

### Restart Both (Quick)
```bash
./start_fullstack.sh
```

## ✅ Verification Checklist

After creating/updating `.env` files:

- [ ] `frontend/.env` exists with `REACT_APP_API_URL`
- [ ] `frontend/.env` has `REACT_APP_WS_URL`
- [ ] `backend/.env` exists
- [ ] Backend can read environment variables
- [ ] Frontend connects to correct port (5002)
- [ ] WebSocket connects successfully
- [ ] Status indicators show correct state
- [ ] Commands execute properly

## 🎯 Current Status

### ✅ Working:
- Frontend reads `REACT_APP_API_URL` correctly
- Frontend reads `REACT_APP_WS_URL` correctly
- Backend runs on port 5002
- REST API integration works
- WebSocket integration works

### ⚠️ Optional:
- Add Gemini API key for advanced AI features
- Customize app name/version
- Enable/disable features via flags

## 📚 References

- [Create React App - Environment Variables](https://create-react-app.dev/docs/adding-custom-environment-variables/)
- [Flask Configuration](https://flask.palletsprojects.com/en/2.3.x/config/)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [Gemini API Keys](https://makersuite.google.com/app/apikey)

---

**Your environment is now properly configured! All variables are integrated and working.** 🚀

