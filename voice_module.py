#!/usr/bin/env python3
"""
Advanced Mini Bash - Voice Control Module (Phase 3)
AI-powered voice recognition with Hindi & English support using Google Cloud APIs
"""

import os
import sys
import json
import subprocess
import threading
import time
from typing import Optional, Dict, List

# Google Cloud imports
try:
    from google.cloud import speech
    from google.cloud import translate_v2 as translate
    from google.cloud import texttospeech
except ImportError:
    print("❌ Google Cloud libraries not installed!")
    print("Run: pip install google-cloud-speech google-cloud-translate google-cloud-texttospeech")
    sys.exit(1)

# Audio recording imports
try:
    import pyaudio
    import wave
except ImportError:
    print("❌ Audio libraries not installed!")
    print("Run: pip install pyaudio wave")
    sys.exit(1)

class VoiceControlledShell:
    def __init__(self, config_file: str = "voice_config.json"):
        """Initialize the voice-controlled shell"""
        self.config = self.load_config(config_file)
        self.speech_client = speech.SpeechClient()
        self.translate_client = translate.Client()
        self.tts_client = texttospeech.TextToSpeechClient()
        
        # Audio settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 5
        
        # Command mappings
        self.hindi_commands = self.load_hindi_commands()
        
        print("🎤 Voice-Controlled Mini Bash initialized!")
        print("💬 Supported languages: Hindi (हिंदी) & English")
        print("🔊 Say 'exit' or 'बाहर निकलो' to quit")
        print("=" * 50)

    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            "google_cloud_credentials": "credentials.json",
            "language_codes": ["hi-IN", "en-US"],
            "voice_feedback": True,
            "auto_translate": True,
            "recording_timeout": 5
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return {**default_config, **json.load(f)}
        else:
            # Create default config file
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config

    def load_hindi_commands(self) -> Dict[str, str]:
        """Load Hindi to English command mappings"""
        hindi_commands = {
            # Basic commands
            "फोल्डर खोलो": "ls",
            "फोल्डर दिखाओ": "ls -la",
            "वर्तमान फोल्डर": "pwd",
            "ऊपर जाओ": "cd ..",
            "घर जाओ": "cd ~",
            "बाहर निकलो": "exit",
            
            # File operations
            "फाइल बनाओ": "touch newfile.txt",
            "फोल्डर बनाओ": "mkdir newfolder",
            "फाइल हटाओ": "rm file.txt",
            "फोल्डर हटाओ": "rmdir folder",
            "फाइल कॉपी करो": "cp source.txt dest.txt",
            "फाइल मूव करो": "mv old.txt new.txt",
            
            # System commands
            "सिस्टम जानकारी": "uname -a",
            "मेमोरी दिखाओ": "free -h",
            "डिस्क स्पेस": "df -h",
            "प्रोसेस दिखाओ": "ps aux",
            
            # Git commands
            "गिट स्टेटस": "git status",
            "गिट कमिट": "git commit -m 'voice commit'",
            "गिट पुश": "git push",
            "गिट पुल": "git pull",
            
            # Network commands
            "इंटरनेट जांचो": "ping google.com",
            "नेटवर्क जानकारी": "ifconfig",
            
            # Custom phrases
            "क्या हो रहा है": "ps aux | head -10",
            "सब कुछ साफ करो": "clear",
            "समय दिखाओ": "date",
            "कैलेंडर दिखाओ": "cal",
        }
        
        # Save to file for reference
        with open("hindi_commands.json", 'w', encoding='utf-8') as f:
            json.dump(hindi_commands, f, indent=2, ensure_ascii=False)
        
        return hindi_commands

    def record_audio(self) -> Optional[str]:
        """Record audio from microphone"""
        try:
            audio = pyaudio.PyAudio()
            
            print("🎤 Listening... (Speak now!)")
            
            stream = audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            frames = []
            for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                data = stream.read(self.CHUNK)
                frames.append(data)
            
            print("⏹️  Recording finished!")
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            # Save audio to temporary file
            temp_file = "temp_audio.wav"
            with wave.open(temp_file, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
            
            return temp_file
            
        except Exception as e:
            print(f"❌ Audio recording error: {e}")
            return None

    def speech_to_text(self, audio_file: str) -> Optional[str]:
        """Convert speech to text using Google Cloud Speech-to-Text"""
        try:
            with open(audio_file, 'rb') as audio_file_content:
                content = audio_file_content.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.RATE,
                language_code="hi-IN",  # Start with Hindi, auto-detect
                alternative_language_codes=["en-US"],
                enable_automatic_punctuation=True,
                model="latest_long"
            )
            
            response = self.speech_client.recognize(config=config, audio=audio)
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                confidence = response.results[0].alternatives[0].confidence
                detected_language = response.results[0].language_code
                
                print(f"🎯 Detected: {detected_language}")
                print(f"📝 Transcript: {transcript}")
                print(f"🎯 Confidence: {confidence:.2%}")
                
                return transcript, detected_language
            
            return None, None
            
        except Exception as e:
            print(f"❌ Speech-to-text error: {e}")
            return None, None

    def translate_text(self, text: str, source_lang: str = "hi", target_lang: str = "en") -> str:
        """Translate text using Google Cloud Translation API"""
        try:
            if source_lang == target_lang:
                return text
                
            result = self.translate_client.translate(
                text, 
                source_language=source_lang, 
                target_language=target_lang
            )
            
            translated = result['translatedText']
            print(f"🌐 Translated: {text} → {translated}")
            return translated
            
        except Exception as e:
            print(f"❌ Translation error: {e}")
            return text

    def map_hindi_command(self, hindi_text: str) -> str:
        """Map Hindi text to English command"""
        hindi_text = hindi_text.lower().strip()
        
        # Direct mapping
        if hindi_text in self.hindi_commands:
            return self.hindi_commands[hindi_text]
        
        # Fuzzy matching for partial commands
        for hindi_cmd, english_cmd in self.hindi_commands.items():
            if hindi_cmd in hindi_text or hindi_text in hindi_cmd:
                return english_cmd
        
        # If no mapping found, return original text
        return hindi_text

    def text_to_speech(self, text: str, language: str = "en") -> None:
        """Convert text to speech for voice feedback"""
        if not self.config.get("voice_feedback", True):
            return
            
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=language,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Save and play audio
            with open("feedback.mp3", "wb") as out:
                out.write(response.audio_content)
            
            # Play feedback (platform specific)
            if sys.platform == "darwin":  # macOS
                subprocess.run(["afplay", "feedback.mp3"], check=False)
            elif sys.platform == "linux":  # Linux
                subprocess.run(["mpg123", "feedback.mp3"], check=False)
            elif sys.platform == "win32":  # Windows
                subprocess.run(["start", "feedback.mp3"], check=False)
            
            # Clean up
            os.remove("feedback.mp3")
            
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")

    def execute_command(self, command: str) -> None:
        """Execute command in the Mini Bash shell"""
        try:
            print(f"🚀 Executing: {command}")
            
            # Send command to Mini Bash via pipe
            process = subprocess.Popen(
                ["./mini-bash"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=command + "\nexit\n")
            
            if stdout:
                print("📤 Output:")
                print(stdout)
            
            if stderr:
                print("⚠️  Errors:")
                print(stderr)
            
            # Voice feedback
            if "error" in stderr.lower() or process.returncode != 0:
                self.text_to_speech("Command failed", "en")
            else:
                self.text_to_speech("Command executed successfully", "en")
                
        except Exception as e:
            print(f"❌ Command execution error: {e}")
            self.text_to_speech("Command execution failed", "en")

    def process_voice_command(self) -> None:
        """Main voice command processing loop"""
        while True:
            try:
                # Record audio
                audio_file = self.record_audio()
                if not audio_file:
                    continue
                
                # Convert speech to text
                transcript, detected_lang = self.speech_to_text(audio_file)
                if not transcript:
                    print("❌ No speech detected")
                    continue
                
                # Clean up audio file
                os.remove(audio_file)
                
                # Check for exit commands
                if any(exit_cmd in transcript.lower() for exit_cmd in ["exit", "quit", "बाहर निकलो", "रुको"]):
                    print("👋 Goodbye!")
                    self.text_to_speech("Goodbye! See you later!", "en")
                    break
                
                # Translate if needed
                if detected_lang and detected_lang.startswith("hi"):
                    # Translate Hindi to English
                    english_text = self.translate_text(transcript, "hi", "en")
                    # Map to command
                    command = self.map_hindi_command(english_text)
                else:
                    # Direct English command
                    command = transcript.strip()
                
                # Execute command
                self.execute_command(command)
                
                print("\n" + "="*50)
                print("🎤 Ready for next command...")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue

    def run(self) -> None:
        """Start the voice-controlled shell"""
        print("🎤 Starting Voice-Controlled Mini Bash...")
        print("Press Ctrl+C to exit")
        
        try:
            self.process_voice_command()
        except KeyboardInterrupt:
            print("\n👋 Voice control stopped!")

def main():
    """Main entry point"""
    print("🔥 Advanced Mini Bash - Voice Control Module (Phase 3)")
    print("=" * 60)
    
    # Check if Mini Bash exists
    if not os.path.exists("./mini-bash"):
        print("❌ Mini Bash executable not found!")
        print("Please run 'make' first to build the shell")
        sys.exit(1)
    
    # Check Google Cloud credentials
    if not os.path.exists("credentials.json"):
        print("❌ Google Cloud credentials not found!")
        print("Please place your credentials.json file in the current directory")
        print("Get it from: https://console.cloud.google.com/apis/credentials")
        sys.exit(1)
    
    # Set environment variable for credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
    
    # Start voice control
    voice_shell = VoiceControlledShell()
    voice_shell.run()

if __name__ == "__main__":
    main()
