# 🚀 HOW TO START - AI Terminal

## ⚡ 3 Simple Steps

### Step 1: Get Gemini API Key (2 minutes)
```bash
# Open in browser:
https://makersuite.google.com/app/apikey

# Click "Create API Key"
# Copy the key (starts with "AI...")
```

### Step 2: Start the App (1 command)
```bash
cd /Users/abhisheksinghrawat/Desktop/bash
./start_fullstack.sh
```

### Step 3: Add Your API Key
```bash
# When prompted, edit this file:
nano backend/.env

# Add your key:
GEMINI_API_KEY=AIza...your_key_here

# Save and exit (Ctrl+X, then Y, then Enter)
```

## 🎉 That's It!

The app will:
- ✅ Build mini-bash (if needed)
- ✅ Install Python dependencies
- ✅ Install Node.js dependencies
- ✅ Start backend on http://localhost:5000
- ✅ Start frontend on http://localhost:3000
- ✅ Open in your browser automatically

## 💬 Try These Commands

### In the Browser Terminal:

**Natural Language:**
```
"show me all python files"
"list files with details"
"go to downloads folder"
"what's in this directory"
```

**Smart File Operations:**
```
"open adi.c in vscode"
"find config.json"
"open package.json in sublime"
```

**Voice Commands:**
```
1. Click 🎤 button
2. Say: "show all files"
3. Watch it work!
```

## 🖥️ What You'll See

### Browser Interface:
```
┌─────────────────────────────────────────────────┐
│ 🤖 AI Terminal        🧠Gemini ✅ 💻Bash ✅    │
├─────────────────────────────────────────────────┤
│ 📁 ~/Desktop/bash                               │
├─────────────────────────────────────────────────┤
│                                                 │
│ ➜ bash $ show me all python files              │
│ 🤖 AI: find . -name "*.py" (95% confident)     │
│ ./shell_bridge.py                              │
│ ./test_voice.py                                │
│ ./voice_module.py                              │
│                                                 │
│ ➜ bash $ open adi.c in vscode                  │
│ 🔍 Searching for adi.c...                      │
│ 📂 Found: /Users/.../projects/adi.c            │
│ 🤖 AI: code /Users/.../projects/adi.c         │
│ ✅ Opened in VS Code                           │
│                                                 │
├─────────────────────────────────────────────────┤
│ $ [Type command...] 🎤 ▶️ Execute             │
└─────────────────────────────────────────────────┘
```

## 📊 System Status Indicators

- **🧠 Gemini AI**: Green = Working, Red = Need API Key
- **💻 Mini Bash**: Green = Built, Red = Need to build
- **🟢 Connected**: WebSocket active
- **⚠️ Processing**: Command executing

## 🎯 Features You Get

### 1. Natural Language Understanding
```
You type: "show python files"
AI thinks: find . -name "*.py"
Terminal executes it ✅
```

### 2. Smart File Finding
```
You type: "open config.json in vscode"
AI searches: Entire computer
AI finds: /path/to/config.json
AI changes directory: cd /path/to
AI opens: code config.json ✅
```

### 3. Voice Control
```
You click: 🎤
You say: "list all files"
AI hears: "list all files"
AI converts: ls -la
Terminal shows: File list ✅
```

### 4. Intelligent Fallback
```
Command → Try mini-bash first
        ↓ (if not supported)
        → Use Mac terminal instead
        ↓
        → Log for improvement ✅
```

## 🔧 Advanced Usage

### Separate Windows
If you want backend and frontend in separate terminals:

**Terminal 1:**
```bash
./start_backend.sh
```

**Terminal 2:**
```bash
./start_frontend.sh
```

### Stop Servers
```bash
# Press Ctrl+C in the terminal running start_fullstack.sh

# Or manually:
pkill -f "python app.py"
pkill -f "react-scripts"
```

### Restart
```bash
# Just run again:
./start_fullstack.sh
```

## 📝 Configuration

### Backend (.env)
```bash
# Required
GEMINI_API_KEY=your_key_here

# Optional (defaults work fine)
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend (.env)
```bash
# Default values (already set)
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=http://localhost:5000
```

## 🐛 Quick Fixes

### "Port 5000 in use"
```bash
lsof -ti:5000 | xargs kill -9
```

### "Port 3000 in use"
```bash
lsof -ti:3000 | xargs kill -9
```

### "Gemini API error"
Check `backend/.env` has correct key with no spaces

### "Mini-bash not found"
```bash
make clean && make
```

## 📚 Need More Help?

Read these guides:
- `QUICK_START_FULLSTACK.md` - Quick start guide
- `FULLSTACK_SETUP.md` - Detailed setup
- `PROJECT_COMPLETE.md` - What's been built
- `README_FULLSTACK.md` - All features

## 🎊 You're Ready!

```bash
./start_fullstack.sh
```

**Then open http://localhost:3000 and start commanding! 🚀**

---

**Questions? Check the logs:**
- Backend errors: `backend.log`
- Frontend errors: `frontend.log`
- Or check browser console (F12)

