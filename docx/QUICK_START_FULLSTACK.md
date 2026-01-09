# 🚀 Quick Start Guide - AI-Powered Terminal

Get your AI-powered terminal running in 5 minutes!

## 📋 What You Need

1. **macOS** (or Linux)
2. **Python 3.8+** - Check: `python3 --version`
3. **Node.js 16+** - Check: `node --version`
4. **Gemini API Key** - Free at https://makersuite.google.com/app/apikey

## ⚡ Super Quick Start (Recommended)

### 1. Get Your Gemini API Key

```bash
# Open this URL in your browser:
open https://makersuite.google.com/app/apikey

# 1. Sign in with your Google account
# 2. Click "Create API Key"
# 3. Copy your API key
```

### 2. Run the Full Stack Setup

```bash
cd /Users/abhisheksinghrawat/Desktop/bash

# Run the all-in-one startup script
./start_fullstack.sh
```

### 3. Add Your API Key

When prompted, edit `backend/.env` and add your API key:

```bash
GEMINI_API_KEY=your_api_key_here
```

### 4. Done! 🎉

The application will automatically:
- ✅ Build mini-bash if needed
- ✅ Install Python dependencies
- ✅ Install Node.js dependencies
- ✅ Start backend on http://localhost:5000
- ✅ Start frontend on http://localhost:3000
- ✅ Open in your browser

## 🎯 Try These Commands

Once the app opens in your browser, try:

### Natural Language
- **"show me all python files"**
- **"list files with details"**
- **"go to downloads folder"**
- **"what's in this directory"**
- **"show disk space"**

### File Operations
- **"find README.md"**
- **"open package.json in vscode"**
- **"search for adi.c and open it"**

### Voice Commands
1. Click the 🎤 microphone button
2. Say: "show me all files"
3. Watch the magic happen!

## 🔧 Manual Setup (If Needed)

### Option A: Separate Terminals

**Terminal 1 - Backend:**
```bash
cd /Users/abhisheksinghrawat/Desktop/bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd /Users/abhisheksinghrawat/Desktop/bash
./start_frontend.sh
```

### Option B: From Scratch

**Build Mini-Bash:**
```bash
cd /Users/abhisheksinghrawat/Desktop/bash
make clean && make
```

**Setup Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**Setup Frontend:**
```bash
cd ../frontend
npm install
```

**Start Backend:**
```bash
cd ../backend
source venv/bin/activate
python app.py
```

**Start Frontend (new terminal):**
```bash
cd frontend
npm start
```

## 🐛 Troubleshooting

### "Port already in use"

**Backend (5000):**
```bash
lsof -ti:5000 | xargs kill -9
```

**Frontend (3000):**
```bash
lsof -ti:3000 | xargs kill -9
```

### "Gemini API error"

1. Check your API key in `backend/.env`
2. Verify it's active: https://makersuite.google.com/app/apikey
3. Make sure there are no extra spaces or quotes

### "mini-bash not found"

```bash
cd /Users/abhisheksinghrawat/Desktop/bash
make clean && make
./mini-bash  # Test it
```

### "Cannot find module"

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Voice input not working

- Use Chrome or Edge browser (Safari has limited support)
- Allow microphone permissions when prompted
- Check browser console (F12) for errors

## 📱 Browser Compatibility

| Feature | Chrome | Edge | Firefox | Safari |
|---------|--------|------|---------|--------|
| Basic UI | ✅ | ✅ | ✅ | ✅ |
| Voice Input | ✅ | ✅ | ❌ | ⚠️ Limited |
| WebSocket | ✅ | ✅ | ✅ | ✅ |

**Recommended:** Chrome or Edge for best experience

## 🎮 Usage Tips

### 1. Natural Language is Smart
Don't overthink it - just type what you want:
- ❌ Bad: `find . -name "*.py" -type f`
- ✅ Good: "show python files"

### 2. File Search is Powerful
The AI will find files anywhere on your system:
- "open config.json in vscode" → Searches entire system
- "find adi.c" → Shows all locations

### 3. Directory Switching is Automatic
No need to `cd` first:
- "open file.txt in sublime" → Auto-navigates to file location

### 4. Fallback is Seamless
If mini-bash doesn't support a command, it automatically uses Mac terminal

## 📊 System Requirements

**Minimum:**
- 4GB RAM
- 2 CPU cores
- 500MB free disk space

**Recommended:**
- 8GB RAM
- 4 CPU cores
- 1GB free disk space
- SSD for faster file search

## 🔐 Security Notes

1. **API Key**: Keep your Gemini API key private
2. **Commands**: Review AI-generated commands before execution
3. **File Access**: The app can access any file your user can access
4. **Network**: Backend needs internet for Gemini API

## 📚 Learn More

- **Full Documentation**: See `FULLSTACK_SETUP.md`
- **API Reference**: http://localhost:5000/api/health
- **Gemini API Docs**: https://ai.google.dev/docs

## 🆘 Need Help?

1. Check logs:
   - Backend: `backend.log`
   - Frontend: `frontend.log`

2. Test components individually:
   ```bash
   # Test mini-bash
   ./mini-bash
   
   # Test backend
   curl http://localhost:5000/api/health
   
   # Test Gemini API
   # (Add your key)
   curl -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY"
   ```

3. Restart everything:
   ```bash
   # Kill all processes
   pkill -f "python app.py"
   pkill -f "react-scripts"
   
   # Start fresh
   ./start_fullstack.sh
   ```

## 🎉 You're Ready!

Enjoy your AI-powered terminal! Type naturally, speak freely, and let Gemini do the work.

**Pro Tip**: Start with simple commands and explore from there. The AI learns from context!

---

**Happy Commanding! 🚀**

