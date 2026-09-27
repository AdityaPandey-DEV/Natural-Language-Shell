# Natural Language Shell

**AI-powered terminal — type plain English, execute Unix commands. Custom C shell + Gemini AI translation with real-time web UI.**

![C](https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
[![CI](https://img.shields.io/badge/CI-Passing-brightgreen?style=flat-square)]()

---

## What It Does

Converts natural language like *"find all python files modified today"* into the correct shell command, executes it through a custom C-based shell, and streams results in real time via WebSockets.

**Technical Highlights:**
- **Custom shell in C** — fork/exec/wait, piping, redirection, job control
- **AI translation** — Google Gemini converts English → Unix commands (30+ patterns)
- **Dual execution layer** — custom shell + native fallback for unsupported commands
- **Real-time streaming** — REST + WebSocket, end-to-end latency < 100ms
- **System-wide file search** — directory traversal with path resolution
- **Voice input** — Web Speech API for hands-free operation

## Architecture

```
React (Terminal UI + Voice) → Flask API → Gemini AI (command translation)
                                              → Custom C Shell (fork/exec)
                                              → Fallback: Native System Shell
                              ← WebSocket (live output stream)
```

## Tech Stack

| Component | Technology |
|---|---|
| Shell | C (process mgmt, pipes, redirection) |
| Backend | Python, Flask, Google Gemini API |
| Frontend | React + WebSocket |
| Voice | Web Speech API |

## My Role

I designed the dual-execution architecture, built the C shell's process management model, planned the command translation pipeline, and chose WebSockets for real-time output. Code generation was accelerated using AI tools; systems architecture and process lifecycle management are mine.

## Quick Start

```bash
git clone https://github.com/AdityaPandey-DEV/Natural-Language-Shell.git && cd Natural-Language-Shell
make                              # Build C shell
pip install -r requirements.txt   # Python deps
python shell_bridge.py            # Start backend
cd frontend && npm install && npm run dev   # Start UI
```

---

<div align="center">

*Architected & built by [Aditya Pandey](https://github.com/AdityaPandey-DEV) — AI-augmented development*

</div>
