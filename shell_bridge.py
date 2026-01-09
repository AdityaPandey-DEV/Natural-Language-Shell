#!/usr/bin/env python3
"""
Advanced Mini Bash - Shell Bridge Module
Communication bridge between Python voice module and C shell
"""

import os
import sys
import subprocess
import threading
import time
import json
from typing import Optional, Dict, List

class ShellBridge:
    def __init__(self, shell_path: str = "./mini-bash"):
        """Initialize the shell bridge"""
        self.shell_path = shell_path
        self.shell_process = None
        self.is_running = False
        
        # Check if shell exists
        if not os.path.exists(shell_path):
            raise FileNotFoundError(f"Shell executable not found: {shell_path}")
    
    def start_shell(self) -> bool:
        """Start the Mini Bash shell process"""
        try:
            self.shell_process = subprocess.Popen(
                [self.shell_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            self.is_running = True
            return True
        except Exception as e:
            print(f"❌ Failed to start shell: {e}")
            return False
    
    def stop_shell(self) -> None:
        """Stop the shell process"""
        if self.shell_process and self.is_running:
            try:
                self.shell_process.stdin.write("exit\n")
                self.shell_process.stdin.flush()
                self.shell_process.terminate()
                self.shell_process.wait(timeout=5)
            except:
                self.shell_process.kill()
            finally:
                self.is_running = False
    
    def execute_command(self, command: str) -> Dict[str, str]:
        """Execute a command directly using subprocess (simpler and more reliable)"""
        if not command or not command.strip():
            return {
                "command": "",
                "output": "",
                "error": "Empty command",
                "success": False
            }
        
        try:
            # Execute command directly using subprocess
            print(f"🔧 Executing: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=os.getcwd()
            )
            
            output = result.stdout.strip()
            error = result.stderr.strip()
            success = result.returncode == 0
            
            print(f"✅ Return code: {result.returncode}")
            if output:
                print(f"📤 Output: {output[:200]}")  # Show first 200 chars
            
            return {
                "command": command,
                "output": output,
                "error": error,
                "success": success
            }
            
        except subprocess.TimeoutExpired:
            return {
                "command": command,
                "output": "",
                "error": "Command timed out",
                "success": False
            }
        except Exception as e:
            return {
                "command": command,
                "output": "",
                "error": str(e),
                "success": False
            }
    
    def execute_commands_batch(self, commands: List[str]) -> List[Dict[str, str]]:
        """Execute multiple commands in sequence"""
        results = []
        for command in commands:
            result = self.execute_command(command)
            results.append(result)
            time.sleep(0.1)  # Small delay between commands
        return results
    
    def get_shell_status(self) -> Dict[str, any]:
        """Get current shell status"""
        return {
            "is_running": self.is_running,
            "shell_path": self.shell_path,
            "pid": self.shell_process.pid if self.shell_process else None
        }

class VoiceCommandProcessor:
    def __init__(self, shell_bridge: ShellBridge):
        """Initialize voice command processor"""
        self.shell_bridge = shell_bridge
        self.command_history = []
        
        # Enhanced command mappings
        self.command_mappings = {
            # Hindi to English mappings
            "hindi": {
                "फोल्डर खोलो": "ls",
                "होल्डर खोलो": "ls",
                "लिस्ट फाइल्स": "ls",
                "लिस्ट फाइल": "ls",
                "फाइल्स दिखाओ": "ls",
                "फाइल दिखाओ": "ls",
                "फोल्डर दिखाओ": "ls -la",
                "वर्तमान फोल्डर": "pwd",
                "ऊपर जाओ": "cd ..",
                "घर जाओ": "cd ~",
                "बाहर निकलो": "exit",
                "फाइल बनाओ": "touch newfile.txt",
                "फोल्डर बनाओ": "mkdir newfolder",
                "फाइल हटाओ": "rm file.txt",
                "फोल्डर हटाओ": "rmdir folder",
                "सिस्टम जानकारी": "uname -a",
                "मेमोरी दिखाओ": "free -h",
                "डिस्क स्पेस": "df -h",
                "प्रोसेस दिखाओ": "ps aux",
                "गिट स्टेटस": "git status",
                "गिट कमिट": "git commit -m 'voice commit'",
                "गिट पुश": "git push",
                "गिट पुल": "git pull",
                "इंटरनेट जांचो": "ping -c 3 google.com",
                "नेटवर्क जानकारी": "ifconfig",
                "क्या हो रहा है": "ps aux | head -10",
                "सब कुछ साफ करो": "clear",
                "समय दिखाओ": "date",
                "कैलेंडर दिखाओ": "cal",
                "हिस्ट्री दिखाओ": "history",
                "जॉब्स दिखाओ": "jobs"
            },
            # English command mappings
            "english": {
                "list files": "ls",
                "list file": "ls",
                "show files": "ls",
                "show file": "ls",
                "files": "ls",
                "show directory": "ls -la",
                "show all files": "ls -la",
                "current directory": "pwd",
                "current folder": "pwd",
                "where am i": "pwd",
                "go up": "cd ..",
                "go home": "cd ~",
                "exit": "exit",
                "quit": "exit",
                "create file": "touch newfile.txt",
                "make file": "touch newfile.txt",
                "create folder": "mkdir newfolder",
                "make folder": "mkdir newfolder",
                "delete file": "rm file.txt",
                "remove file": "rm file.txt",
                "delete folder": "rmdir folder",
                "remove folder": "rmdir folder",
                "system info": "uname -a",
                "system information": "uname -a",
                "show memory": "free -h",
                "disk space": "df -h",
                "show processes": "ps aux",
                "git status": "git status",
                "git commit": "git commit -m 'voice commit'",
                "git push": "git push",
                "git pull": "git pull",
                "check internet": "ping -c 3 google.com",
                "network info": "ifconfig",
                "what's running": "ps aux | head -10",
                "clear screen": "clear",
                "show time": "date",
                "show calendar": "cal",
                "show history": "history",
                "show jobs": "jobs"
            }
        }
    
    def process_voice_command(self, voice_text: str, language: str = "auto") -> Dict[str, str]:
        """Process voice command and return execution result"""
        # Detect language if auto
        if language == "auto":
            language = self.detect_language(voice_text)
        
        # Map command
        mapped_command = self.map_command(voice_text, language)
        print(f"🗺️  Mapping: '{voice_text}' ({language}) → '{mapped_command}'")
        
        # Execute command
        result = self.shell_bridge.execute_command(mapped_command)
        result["mapped_command"] = mapped_command  # Add mapped command to result
        
        # Add to history
        self.command_history.append({
            "voice_text": voice_text,
            "mapped_command": mapped_command,
            "language": language,
            "timestamp": time.time(),
            "result": result
        })
        
        return result
    
    def detect_language(self, text: str) -> str:
        """Detect if text is Hindi or English"""
        # Simple detection based on character sets
        hindi_chars = set("अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह")
        text_chars = set(text)
        
        if text_chars.intersection(hindi_chars):
            return "hindi"
        else:
            return "english"
    
    def map_command(self, text: str, language: str) -> str:
        """Map voice text to shell command"""
        # Clean the text - remove punctuation and extra spaces
        import re
        text_clean = re.sub(r'[!.?।]', '', text).strip().lower()
        
        # Check direct mappings
        if language in self.command_mappings:
            # Try exact match first
            if text_clean in self.command_mappings[language]:
                return self.command_mappings[language][text_clean]
            
            # Try fuzzy matching
            for voice_cmd, shell_cmd in self.command_mappings[language].items():
                voice_cmd_clean = re.sub(r'[!.?।]', '', voice_cmd).lower()
                if voice_cmd_clean in text_clean or text_clean in voice_cmd_clean:
                    return shell_cmd
            
            # Try matching individual words
            words = text_clean.split()
            for voice_cmd, shell_cmd in self.command_mappings[language].items():
                voice_words = voice_cmd.lower().split()
                if any(word in words for word in voice_words):
                    # Check if at least 50% of words match
                    matches = sum(1 for word in voice_words if word in words)
                    if matches >= len(voice_words) / 2:
                        return shell_cmd
        
        # If no mapping found, return cleaned text
        return text_clean if text_clean else text
    
    def get_command_history(self) -> List[Dict[str, any]]:
        """Get command execution history"""
        return self.command_history
    
    def clear_history(self) -> None:
        """Clear command history"""
        self.command_history.clear()

def main():
    """Test the shell bridge"""
    print("🔗 Testing Shell Bridge...")
    
    try:
        # Initialize bridge
        bridge = ShellBridge()
        
        # Start shell
        if bridge.start_shell():
            print("✅ Shell started successfully")
            
            # Test commands
            test_commands = [
                "pwd",
                "ls",
                "echo 'Hello from bridge!'",
                "history"
            ]
            
            processor = VoiceCommandProcessor(bridge)
            
            for cmd in test_commands:
                print(f"\n🚀 Testing: {cmd}")
                result = processor.process_voice_command(cmd, "english")
                print(f"📤 Output: {result['output']}")
                if result['error']:
                    print(f"⚠️  Error: {result['error']}")
            
            # Stop shell
            bridge.stop_shell()
            print("\n✅ Shell stopped")
            
        else:
            print("❌ Failed to start shell")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
