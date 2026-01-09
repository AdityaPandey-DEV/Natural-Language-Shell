#!/usr/bin/env python3
"""
AI-Powered Terminal Backend
Full-stack bash shell with Gemini API integration
"""

import os
import sys
import json
import subprocess
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global state
current_directory = os.getcwd()
command_history = []
feedback_log = []

# Initialize Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    print("⚠️  Warning: GEMINI_API_KEY not set. Natural language processing will be limited.")
    model = None


class CommandProcessor:
    """Process natural language commands using Gemini AI"""
    
    def __init__(self, mini_bash_path: str = "../mini-bash"):
        self.mini_bash_path = mini_bash_path
        self.mini_bash_available = os.path.exists(mini_bash_path)
        
    def convert_natural_language_to_command(self, text: str, current_dir: str) -> Dict:
        """Use Gemini AI to convert natural language to terminal command"""
        global model
        
        if not model:
            return {
                "command": text,
                "explanation": "Direct command (Gemini not configured)",
                "confidence": 0.5,
                "needs_file_search": False
            }
        
        prompt = f"""You are an AI assistant that converts natural language instructions into terminal commands.
        
Current directory: {current_dir}
User request: "{text}"

Analyze the request and provide a JSON response with:
1. "command": The exact terminal command to execute (macOS/Linux compatible)
2. "explanation": Brief explanation of what the command does
3. "confidence": Confidence level (0.0-1.0)
4. "needs_file_search": true if we need to search for a file/directory first, false otherwise
5. "target_file": If needs_file_search is true, what file/folder to search for
6. "action_type": One of: "execute", "open_file", "open_app", "change_directory", "search"

Examples:
- "show me all python files" → {{"command": "find . -name '*.py'", "explanation": "Find all Python files", "confidence": 0.95, "needs_file_search": false}}
- "open adi.c in vscode" → {{"command": "code", "explanation": "Open file in VS Code", "confidence": 0.9, "needs_file_search": true, "target_file": "adi.c", "action_type": "open_file"}}
- "list all files" → {{"command": "ls -la", "explanation": "List all files with details", "confidence": 1.0, "needs_file_search": false}}
- "go to downloads folder" → {{"command": "cd ~/Downloads", "explanation": "Change to Downloads directory", "confidence": 0.95, "needs_file_search": false, "action_type": "change_directory"}}

IMPORTANT: 
- For file operations, use macOS/Linux commands
- If opening files in apps, provide the app command (code, open, subl, etc.)
- Return ONLY valid JSON, no additional text

JSON Response:"""

        try:
            response = model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            return result
            
        except Exception as e:
            print(f"❌ Gemini AI error: {e}")
            # Fallback to basic command mapping
            return self._fallback_command_mapping(text)
    
    def _fallback_command_mapping(self, text: str) -> Dict:
        """Fallback command mapping when Gemini is unavailable"""
        text_lower = text.lower()
        
        # Basic command mappings
        mappings = {
            "list files": "ls -la",
            "show files": "ls -la",
            "current directory": "pwd",
            "current folder": "pwd",
            "where am i": "pwd",
            "go home": "cd ~",
            "go back": "cd ..",
            "clear screen": "clear",
            "show processes": "ps aux",
            "disk space": "df -h",
            "memory usage": "free -h",
            "system info": "uname -a",
        }
        
        for phrase, command in mappings.items():
            if phrase in text_lower:
                return {
                    "command": command,
                    "explanation": f"Execute {command}",
                    "confidence": 0.8,
                    "needs_file_search": False
                }
        
        # Check if it's a file opening request
        if "open" in text_lower:
            words = text_lower.split()
            if len(words) >= 2:
                return {
                    "command": "open",
                    "explanation": "Open file or directory",
                    "confidence": 0.7,
                    "needs_file_search": True,
                    "target_file": words[-1] if "in" not in words[-1] else words[words.index("open") + 1]
                }
        
        # Default: treat as direct command
        return {
            "command": text,
            "explanation": "Direct command execution",
            "confidence": 0.6,
            "needs_file_search": False
        }
    
    def search_file_system(self, filename: str, start_dir: str = "/") -> List[str]:
        """Search for a file across the system"""
        print(f"🔍 Searching for '{filename}' starting from {start_dir}")
        
        results = []
        search_paths = [
            os.path.expanduser("~"),  # Home directory
            "/Users",  # macOS users
            "/Applications",  # macOS apps
            start_dir  # Current directory
        ]
        
        # Use find command for faster search
        for search_path in search_paths:
            try:
                # Limit search depth to avoid performance issues
                cmd = f"find '{search_path}' -maxdepth 5 -name '{filename}' 2>/dev/null"
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.stdout:
                    found_paths = result.stdout.strip().split('\n')
                    results.extend([p for p in found_paths if p])
                    
            except Exception as e:
                print(f"⚠️  Search error in {search_path}: {e}")
                continue
        
        # Remove duplicates and limit results
        results = list(set(results))[:10]
        print(f"✅ Found {len(results)} matches")
        return results
    
    def execute_in_mini_bash(self, command: str) -> Dict:
        """Execute command in mini-bash"""
        if not self.mini_bash_available:
            return {
                "success": False,
                "output": "",
                "error": "mini-bash not available",
                "executor": "none"
            }
        
        # Mini-bash now supports file operations natively!
        # No need to redirect anymore
        
        try:
            process = subprocess.Popen(
                [self.mini_bash_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=current_directory
            )
            
            stdout, stderr = process.communicate(input=f"{command}\nexit\n", timeout=10)
            
            # Clean up mini-bash prompt output
            output_lines = stdout.strip().split('\n')
            cleaned_output = []
            for line in output_lines:
                # Skip mini-bash welcome message and prompts
                if 'Advanced Mini Bash Shell' not in line and \
                   'Type \'exit\' to quit' not in line and \
                   'mini-bash:' not in line and \
                   line.strip():
                    cleaned_output.append(line)
            
            final_output = '\n'.join(cleaned_output).strip()
            
            # For file operations that don't produce output, add success message
            if not final_output and command.split()[0] in ['mkdir', 'rmdir', 'touch', 'rm', 'cp', 'mv']:
                final_output = f"✅ Command '{command}' executed successfully"
            
            return {
                "success": process.returncode == 0,
                "output": final_output,
                "error": stderr.strip(),
                "executor": "mini-bash"
            }
            
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                "success": False,
                "output": "",
                "error": "Command timed out",
                "executor": "mini-bash"
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "executor": "mini-bash"
            }
    
    def execute_in_system_terminal(self, command: str) -> Dict:
        """Execute command in system terminal (Mac/Linux)"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=current_directory
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "error": result.stderr.strip(),
                "executor": "system-terminal"
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "Command timed out",
                "executor": "system-terminal"
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "executor": "system-terminal"
            }
    
    def execute_command(self, command: str, prefer_mini_bash: bool = True) -> Dict:
        """Execute command with fallback logic or force specific executor"""
        global current_directory, feedback_log
        
        # Handle directory change
        if command.startswith("cd "):
            target_dir = command[3:].strip()
            target_dir = os.path.expanduser(target_dir)
            
            try:
                if os.path.isdir(target_dir):
                    os.chdir(target_dir)
                    current_directory = os.getcwd()
                    return {
                        "success": True,
                        "output": f"Changed directory to {current_directory}",
                        "error": "",
                        "executor": "built-in"
                    }
                else:
                    return {
                        "success": False,
                        "output": "",
                        "error": f"Directory not found: {target_dir}",
                        "executor": "built-in"
                    }
            except Exception as e:
                return {
                    "success": False,
                    "output": "",
                    "error": str(e),
                    "executor": "built-in"
                }
        
        # Try mini-bash first
        if prefer_mini_bash and self.mini_bash_available:
            result = self.execute_in_mini_bash(command)
            
            # If mini-bash fails, try system terminal
            if not result["success"]:
                print(f"⚠️  mini-bash failed, trying system terminal...")
                system_result = self.execute_in_system_terminal(command)
                
                if system_result["success"]:
                    # Log feedback: command not supported in mini-bash
                    feedback_log.append({
                        "timestamp": datetime.now().isoformat(),
                        "command": command,
                        "status": "not_implemented_in_mini_bash",
                        "error": result["error"]
                    })
                    return system_result
                
                return result
            
            return result
        else:
            # Use system terminal directly
            return self.execute_in_system_terminal(command)


# Initialize command processor
command_processor = CommandProcessor()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "gemini_available": model is not None,
        "mini_bash_available": command_processor.mini_bash_available,
        "current_directory": current_directory
    })


@app.route('/api/directory', methods=['GET'])
def get_directory():
    """Get current directory"""
    return jsonify({
        "current_directory": current_directory,
        "home_directory": os.path.expanduser("~"),
        "exists": os.path.exists(current_directory)
    })


@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute a natural language or direct command"""
    global current_directory, command_history
    
    data = request.json
    user_input = data.get('command', '').strip()
    is_voice = data.get('is_voice', False)
    preferred_executor = data.get('preferred_executor', 'mini-bash')  # 'mini-bash' or 'system-terminal'
    
    if not user_input:
        return jsonify({"error": "No command provided"}), 400
    
    print(f"\n{'🎤' if is_voice else '⌨️ '} User input: {user_input}")
    
    # Convert natural language to command
    ai_result = command_processor.convert_natural_language_to_command(user_input, current_directory)
    command = ai_result["command"]
    
    print(f"🤖 AI interpretation: {command}")
    print(f"📊 Confidence: {ai_result['confidence']:.2%}")
    
    # Handle file search if needed
    if ai_result.get("needs_file_search"):
        target_file = ai_result.get("target_file")
        if target_file:
            print(f"🔍 Searching for file: {target_file}")
            search_results = command_processor.search_file_system(target_file, current_directory)
            
            if search_results:
                file_path = search_results[0]  # Use first match
                file_dir = os.path.dirname(file_path)
                
                # Change to that directory
                if file_dir and os.path.isdir(file_dir):
                    os.chdir(file_dir)
                    current_directory = os.getcwd()
                    print(f"📂 Changed to directory: {current_directory}")
                
                # Modify command to use found file
                if "open" in user_input.lower():
                    app_name = "open"  # Default macOS open
                    if "vscode" in user_input.lower() or "code" in user_input.lower():
                        app_name = "code"
                    elif "sublime" in user_input.lower():
                        app_name = "subl"
                    
                    command = f"{app_name} '{file_path}'"
                
                ai_result["search_results"] = search_results
                ai_result["selected_file"] = file_path
            else:
                return jsonify({
                    "success": False,
                    "error": f"File not found: {target_file}",
                    "command": command,
                    "ai_interpretation": ai_result
                }), 404
    
    # Execute command with preferred executor
    prefer_mini_bash = (preferred_executor == 'mini-bash')
    result = command_processor.execute_command(command, prefer_mini_bash=prefer_mini_bash)
    
    # Add to history
    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "command": command,
        "is_voice": is_voice,
        "result": result,
        "ai_interpretation": ai_result,
        "directory": current_directory
    }
    command_history.append(history_entry)
    
    # Emit to WebSocket clients
    socketio.emit('command_executed', history_entry)
    
    return jsonify({
        "success": result["success"],
        "output": result["output"],
        "error": result["error"],
        "executor": result["executor"],
        "command": command,
        "ai_interpretation": ai_result,
        "current_directory": current_directory
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get command history"""
    limit = request.args.get('limit', 50, type=int)
    return jsonify({
        "history": command_history[-limit:],
        "total": len(command_history)
    })


@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    """Get feedback log (commands not supported in mini-bash)"""
    return jsonify({
        "feedback": feedback_log,
        "total": len(feedback_log)
    })


@app.route('/api/search', methods=['POST'])
def search_files():
    """Search for files in the system"""
    data = request.json
    filename = data.get('filename', '').strip()
    start_dir = data.get('start_dir', current_directory)
    
    if not filename:
        return jsonify({"error": "No filename provided"}), 400
    
    results = command_processor.search_file_system(filename, start_dir)
    
    return jsonify({
        "results": results,
        "count": len(results),
        "search_term": filename
    })


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('✅ Client connected')
    emit('connected', {
        "status": "connected",
        "current_directory": current_directory
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('❌ Client disconnected')


@socketio.on('execute_command')
def handle_ws_command(data):
    """Handle command execution via WebSocket"""
    user_input = data.get('command', '').strip()
    is_voice = data.get('is_voice', False)
    
    if not user_input:
        emit('error', {"error": "No command provided"})
        return
    
    # Process command (same as REST API)
    # ... (similar logic to execute_command endpoint)
    emit('command_result', {"status": "processing", "command": user_input})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AI-Powered Terminal Backend Starting...")
    print("="*60)
    print(f"📂 Current Directory: {current_directory}")
    print(f"🤖 Gemini AI: {'✅ Available' if model else '❌ Not configured'}")
    print(f"💻 Mini-Bash: {'✅ Available' if command_processor.mini_bash_available else '❌ Not found'}")
    print("="*60)
    print("🌐 Server starting on http://localhost:5002")
    print("📡 WebSocket available on ws://localhost:5002")
    print("="*60 + "\n")
    
    socketio.run(app, host='0.0.0.0', port=5002, debug=True, allow_unsafe_werkzeug=True)

