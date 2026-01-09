# Natural Language Shell Interface
**AI-Assisted Command Translation & Execution System**

A system-level application that enables users to interact with a Unix/Linux terminal using natural language. The system translates user instructions into executable shell commands using AI, executes them via a custom C-based shell, and streams results in real time through a web interface.

---

## 📌 Overview

Natural Language Shell Interface combines **Operating Systems fundamentals**, **shell programming**, and **AI-assisted command processing** to simplify terminal usage while preserving execution reliability and system-level control.

This project demonstrates:
- Custom shell implementation in **C**
- Process execution and command parsing
- Client–server architecture with real-time communication
- Practical application of AI in systems software

---

## ✨ Features

### 🖥 Natural Language Command Execution
- Converts plain English instructions into valid Unix/Linux commands
- Supports file operations, navigation, search, and system commands
- Handles **30+ command patterns**

### ⚙️ Custom Mini-Bash Shell (C)
- Implements command parsing, execution, and error handling
- Automatic fallback to native system shell for unsupported commands
- Ensures reliable execution on **Linux/macOS**

### 🔁 Real-Time Execution Pipeline
- REST APIs for command handling
- WebSockets for live output streaming
- End-to-end latency under **100 ms**

### 📂 System-Wide File Search
- Searches across directories
- Automatic path resolution
- Application-aware file opening (e.g., VS Code)

### 🎙 Optional Voice Input
- Browser-based speech recognition
- Hands-free command execution
- Asynchronous execution handling

---

## 🏗 Architecture

The system follows a modular **client–server architecture** with a dual execution layer to ensure reliability and OS-level control.

```
Frontend (React)
│
├── Natural Language Input
├── Terminal UI
├── WebSocket Client
│
└── REST / WebSocket APIs
        ↓
Backend (Python / Flask)
│
├── AI Command Translation (Google Gemini)
├── Command Dispatcher & Validation
├── System-Wide File Search Engine
├── Execution Controller
│
└── Dual Execution Layer
        ├── Custom Mini-Bash (C)
        └── Native System Shell (Linux / macOS)
```

---

## ⚙️ Backend Setup

### Prerequisites
- Python 3.8+
- pip
- Linux or macOS

### Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5002
CORS_ORIGINS=http://localhost:3000
```

Run backend:
```bash
python app.py
```

---

## 🎨 Frontend Setup

```bash
cd frontend
npm install
npm start
```

Open:
```
http://localhost:3000
```

---

## 📄 License
MIT License

---

## 👤 Author
Aditya Pandey  
Computer Science Undergraduate  
Focus: Operating Systems, Systems Programming, Scalable Software Engineering
