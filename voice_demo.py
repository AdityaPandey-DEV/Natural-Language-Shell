#!/usr/bin/env python3
"""
Advanced Mini Bash - Voice Control Demo Script
Interactive demo showcasing Hindi and English voice commands
"""

import os
import sys
import time
import subprocess
from typing import List, Dict

class VoiceDemo:
    def __init__(self):
        """Initialize the voice demo"""
        self.demo_commands = {
            "hindi": [
                "फोल्डर खोलो",
                "वर्तमान फोल्डर", 
                "सिस्टम जानकारी",
                "समय दिखाओ",
                "हिस्ट्री दिखाओ"
            ],
            "english": [
                "list files",
                "current directory",
                "system info", 
                "show time",
                "show history"
            ]
        }
        
        self.expected_outputs = {
            "फोल्डर खोलो": "ls",
            "वर्तमान फोल्डर": "pwd",
            "सिस्टम जानकारी": "uname -a",
            "समय दिखाओ": "date",
            "हिस्ट्री दिखाओ": "history",
            "list files": "ls",
            "current directory": "pwd", 
            "system info": "uname -a",
            "show time": "date",
            "show history": "history"
        }

    def print_banner(self):
        """Print demo banner"""
        print("🔥" + "="*68 + "🔥")
        print("🎤 Advanced Mini Bash - Voice Control Demo (Phase 3)")
        print("🔥" + "="*68 + "🔥")
        print()
        print("🌟 Features Demonstrated:")
        print("   • Hindi Voice Commands (हिंदी आवाज़ कमांड)")
        print("   • English Voice Commands")
        print("   • Google Cloud Speech-to-Text")
        print("   • Google Cloud Translation")
        print("   • Google Cloud Text-to-Speech")
        print("   • Real-time Command Execution")
        print()

    def check_dependencies(self) -> bool:
        """Check if all dependencies are available"""
        print("🔍 Checking dependencies...")
        
        # Check Mini Bash
        if not os.path.exists("./mini-bash"):
            print("❌ Mini Bash not found! Run 'make' first.")
            return False
        print("✅ Mini Bash found")
        
        # Check Google Cloud credentials
        if not os.path.exists("credentials.json"):
            print("❌ Google Cloud credentials not found!")
            print("   Please place credentials.json in current directory")
            return False
        print("✅ Google Cloud credentials found")
        
        # Check Python modules
        try:
            import google.cloud.speech
            import google.cloud.translate_v2
            import google.cloud.texttospeech
            import pyaudio
            print("✅ Google Cloud libraries found")
        except ImportError as e:
            print(f"❌ Missing Python libraries: {e}")
            print("   Run: pip install -r requirements.txt")
            return False
        
        return True

    def show_voice_commands(self):
        """Show available voice commands"""
        print("🎤 Available Voice Commands:")
        print()
        
        print("🇮🇳 Hindi Commands (हिंदी):")
        for i, cmd in enumerate(self.demo_commands["hindi"], 1):
            print(f"   {i}. \"{cmd}\" → {self.expected_outputs[cmd]}")
        print()
        
        print("🇺🇸 English Commands:")
        for i, cmd in enumerate(self.demo_commands["english"], 1):
            print(f"   {i}. \"{cmd}\" → {self.expected_outputs[cmd]}")
        print()

    def run_interactive_demo(self):
        """Run interactive demo"""
        print("🎮 Interactive Demo Mode")
        print("=" * 30)
        print()
        print("Choose an option:")
        print("1. 🎤 Start Voice Control (Real-time)")
        print("2. 🧪 Test Commands (Simulated)")
        print("3. 📚 Show Command Examples")
        print("4. ❌ Exit")
        print()
        
        while True:
            try:
                choice = input("Enter your choice (1-4): ").strip()
                
                if choice == "1":
                    self.start_voice_control()
                    break
                elif choice == "2":
                    self.run_simulated_demo()
                    break
                elif choice == "3":
                    self.show_voice_commands()
                    continue
                elif choice == "4":
                    print("👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-4.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

    def start_voice_control(self):
        """Start real voice control"""
        print("🎤 Starting Voice Control...")
        print("Make sure your microphone is working!")
        print("Press Ctrl+C to stop")
        print()
        
        try:
            # Import and run the enhanced voice module
            from voice_enhanced import EnhancedVoiceShell
            
            voice_shell = EnhancedVoiceShell()
            voice_shell.run()
            
        except ImportError:
            print("❌ Voice module not found!")
            print("Make sure voice_enhanced.py is in the current directory")
        except Exception as e:
            print(f"❌ Error starting voice control: {e}")

    def run_simulated_demo(self):
        """Run simulated demo without actual voice input"""
        print("🧪 Simulated Demo Mode")
        print("=" * 25)
        print()
        print("This will simulate voice commands without using the microphone.")
        print()
        
        # Test Hindi commands
        print("🇮🇳 Testing Hindi Commands:")
        for cmd in self.demo_commands["hindi"]:
            print(f"\n🎤 Simulated: \"{cmd}\"")
            print(f"🔄 Mapped to: {self.expected_outputs[cmd]}")
            
            # Execute the command
            try:
                result = subprocess.run(
                    ["./mini-bash"],
                    input=f"{self.expected_outputs[cmd]}\nexit\n",
                    text=True,
                    capture_output=True,
                    timeout=5
                )
                
                if result.stdout:
                    print("📤 Output:")
                    print(result.stdout)
                if result.stderr:
                    print("⚠️  Error:")
                    print(result.stderr)
                    
            except subprocess.TimeoutExpired:
                print("⏰ Command timed out")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            time.sleep(1)
        
        print("\n" + "="*50)
        
        # Test English commands
        print("🇺🇸 Testing English Commands:")
        for cmd in self.demo_commands["english"]:
            print(f"\n🎤 Simulated: \"{cmd}\"")
            print(f"🔄 Mapped to: {self.expected_outputs[cmd]}")
            
            # Execute the command
            try:
                result = subprocess.run(
                    ["./mini-bash"],
                    input=f"{self.expected_outputs[cmd]}\nexit\n",
                    text=True,
                    capture_output=True,
                    timeout=5
                )
                
                if result.stdout:
                    print("📤 Output:")
                    print(result.stdout)
                if result.stderr:
                    print("⚠️  Error:")
                    print(result.stderr)
                    
            except subprocess.TimeoutExpired:
                print("⏰ Command timed out")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            time.sleep(1)
        
        print("\n✅ Simulated demo completed!")

    def show_setup_instructions(self):
        """Show setup instructions"""
        print("📋 Setup Instructions:")
        print("=" * 25)
        print()
        print("1. 🔧 Install Dependencies:")
        print("   pip install -r requirements.txt")
        print()
        print("2. 🔑 Get Google Cloud Credentials:")
        print("   • Go to: https://console.cloud.google.com/apis/credentials")
        print("   • Create a service account")
        print("   • Download JSON key file")
        print("   • Rename to 'credentials.json'")
        print()
        print("3. 🎤 Test Microphone:")
        print("   • Make sure your microphone is working")
        print("   • Test with: python3 test_voice.py")
        print()
        print("4. 🚀 Run Voice Control:")
        print("   • python3 voice_enhanced.py")
        print("   • Or: python3 voice_demo.py")
        print()

    def run(self):
        """Run the complete demo"""
        self.print_banner()
        
        if not self.check_dependencies():
            print("\n❌ Dependencies check failed!")
            self.show_setup_instructions()
            return
        
        print("✅ All dependencies ready!")
        print()
        
        self.show_voice_commands()
        self.run_interactive_demo()

def main():
    """Main entry point"""
    demo = VoiceDemo()
    demo.run()

if __name__ == "__main__":
    main()
