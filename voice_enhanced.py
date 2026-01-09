#!/usr/bin/env python3
"""
Advanced Mini Bash - Enhanced Voice Control Module (Phase 3)
AI-powered voice recognition with Hindi & English support using Google Cloud APIs
Enhanced with better shell integration and command processing
"""

import os
import sys
import json
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

# Import our shell bridge
from shell_bridge import ShellBridge, VoiceCommandProcessor

class EnhancedVoiceShell:
    def __init__(self, config_file: str = "voice_config.json"):
        """Initialize the enhanced voice-controlled shell"""
        self.config = self.load_config(config_file)
        self.speech_client = speech.SpeechClient()
        self.translate_client = translate.Client()
        self.tts_client = texttospeech.TextToSpeechClient()
        
        # Initialize shell bridge
        self.shell_bridge = ShellBridge()
        self.command_processor = None
        
        # Audio settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 5
        
        # Voice control state
        self.is_listening = False
        self.is_processing = False
        
        print("🎤 Enhanced Voice-Controlled Mini Bash initialized!")
        print("💬 Supported languages: Hindi (हिंदी) & English")
        print("🔊 Say 'exit' or 'बाहर निकलो' to quit")
        print("=" * 60)

    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            "google_cloud_credentials": "credentials.json",
            "language_codes": ["hi-IN", "en-US"],
            "voice_feedback": True,
            "auto_translate": True,
            "recording_timeout": 5,
            "confidence_threshold": 0.7,
            "continuous_listening": False
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return {**default_config, **json.load(f)}
        else:
            # Create default config file
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config

    def start_shell(self) -> bool:
        """Start the Mini Bash shell"""
        if self.shell_bridge.start_shell():
            self.command_processor = VoiceCommandProcessor(self.shell_bridge)
            print("✅ Mini Bash shell started")
            return True
        else:
            print("❌ Failed to start Mini Bash shell")
            return False

    def stop_shell(self) -> None:
        """Stop the Mini Bash shell"""
        self.shell_bridge.stop_shell()
        print("✅ Mini Bash shell stopped")

    def record_audio(self) -> Optional[str]:
        """Record audio from microphone with enhanced error handling"""
        try:
            audio = pyaudio.PyAudio()
            
            # Check for available audio devices
            device_count = audio.get_device_count()
            if device_count == 0:
                print("❌ No audio devices found!")
                return None
            
            print("🎤 Listening... (Speak now!)")
            self.is_listening = True
            
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
            self.is_listening = False
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            # Save audio to temporary file
            temp_file = f"temp_audio_{int(time.time())}.wav"
            with wave.open(temp_file, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
            
            return temp_file
            
        except Exception as e:
            print(f"❌ Audio recording error: {e}")
            self.is_listening = False
            return None

    def speech_to_text(self, audio_file: str) -> tuple[Optional[str], Optional[str]]:
        """Convert speech to text using Google Cloud Speech-to-Text with enhanced config"""
        try:
            with open(audio_file, 'rb') as audio_file_content:
                content = audio_file_content.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.RATE,
                language_code="hi-IN",  # Start with Hindi
                alternative_language_codes=["en-US"],
                enable_automatic_punctuation=True,
                enable_word_time_offsets=True,
                model="latest_long",
                use_enhanced=True
            )
            
            response = self.speech_client.recognize(config=config, audio=audio)
            
            if response.results:
                result = response.results[0]
                transcript = result.alternatives[0].transcript
                confidence = result.alternatives[0].confidence
                detected_language = result.language_code
                
                print(f"🎯 Detected Language: {detected_language}")
                print(f"📝 Transcript: {transcript}")
                print(f"🎯 Confidence: {confidence:.2%}")
                
                # Check confidence threshold
                if confidence < self.config.get("confidence_threshold", 0.7):
                    print("⚠️  Low confidence, please try again")
                    return None, None
                
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

    def text_to_speech(self, text: str, language: str = "en") -> None:
        """Convert text to speech for voice feedback with enhanced voice selection"""
        if not self.config.get("voice_feedback", True):
            return
            
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Select appropriate voice based on language
            if language.startswith("hi"):
                voice = texttospeech.VoiceSelectionParams(
                    language_code="hi-IN",
                    name="hi-IN-Wavenet-A",  # Hindi voice
                    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
                )
            else:
                voice = texttospeech.VoiceSelectionParams(
                    language_code="en-US",
                    name="en-US-Wavenet-D",  # English voice
                    ssml_gender=texttospeech.SsmlVoiceGender.MALE
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
            feedback_file = f"feedback_{int(time.time())}.mp3"
            with open(feedback_file, "wb") as out:
                out.write(response.audio_content)
            
            # Play feedback (platform specific)
            self.play_audio(feedback_file)
            
            # Clean up
            os.remove(feedback_file)
            
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")

    def play_audio(self, audio_file: str) -> None:
        """Play audio file (platform specific)"""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["afplay", audio_file], check=False, capture_output=True)
            elif sys.platform == "linux":  # Linux
                subprocess.run(["mpg123", audio_file], check=False, capture_output=True)
            elif sys.platform == "win32":  # Windows
                subprocess.run(["start", audio_file], check=False, capture_output=True)
        except:
            pass  # Silently fail if audio player not available

    def process_voice_command(self) -> None:
        """Main voice command processing loop with enhanced features"""
        print("🎤 Voice control ready! Start speaking...")
        
        while True:
            try:
                # Record audio
                audio_file = self.record_audio()
                if not audio_file:
                    continue
                
                # Convert speech to text
                transcript, detected_lang = self.speech_to_text(audio_file)
                if not transcript:
                    print("❌ No speech detected or low confidence")
                    continue
                
                # Clean up audio file
                os.remove(audio_file)
                
                # Check for exit commands
                exit_commands = ["exit", "quit", "stop", "बाहर निकलो", "रुको", "बंद करो"]
                if any(exit_cmd in transcript.lower() for exit_cmd in exit_commands):
                    print("👋 Goodbye!")
                    self.text_to_speech("Goodbye! See you later!", "en")
                    break
                
                # Process command
                self.is_processing = True
                print("🔄 Processing command...")
                
                # Determine language
                if detected_lang and detected_lang.startswith("hi"):
                    language = "hindi"
                    # Translate if needed
                    english_text = self.translate_text(transcript, "hi", "en")
                    print(f"📝 Original (Hindi): {transcript}")
                    print(f"🌐 Translated (English): {english_text}")
                else:
                    language = "english"
                    english_text = transcript
                    print(f"📝 Command (English): {english_text}")
                
                # Execute command using shell bridge
                print(f"🎯 Language detected: {language}")
                result = self.command_processor.process_voice_command(transcript, language)
                print(f"🔧 Mapped command: {result.get('mapped_command', 'N/A')}")
                
                # Display results
                if result.get("success", False):
                    print("✅ Command executed successfully!")
                    if result.get("output"):
                        print("📤 Output:")
                        print(result["output"])
                    
                    # Voice feedback
                    if language == "hindi":
                        self.text_to_speech("कमांड सफलतापूर्वक चलाया गया", "hi")
                    else:
                        self.text_to_speech("Command executed successfully", "en")
                else:
                    print("❌ Command failed!")
                    if result.get("error"):
                        print("⚠️  Error:")
                        print(result["error"])
                    
                    # Voice feedback
                    if language == "hindi":
                        self.text_to_speech("कमांड असफल", "hi")
                    else:
                        self.text_to_speech("Command failed", "en")
                
                self.is_processing = False
                
                print("\n" + "="*60)
                print("🎤 Ready for next command...")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.is_processing = False
                continue

    def show_status(self) -> None:
        """Show current status of the voice shell"""
        print("\n📊 Voice Shell Status:")
        print(f"   Listening: {'Yes' if self.is_listening else 'No'}")
        print(f"   Processing: {'Yes' if self.is_processing else 'No'}")
        print(f"   Shell Running: {'Yes' if self.shell_bridge.is_running else 'No'}")
        
        if self.command_processor:
            history = self.command_processor.get_command_history()
            print(f"   Commands Executed: {len(history)}")
            
            if history:
                print("   Recent Commands:")
                for cmd in history[-3:]:  # Show last 3 commands
                    print(f"     - {cmd['voice_text']} → {cmd['mapped_command']}")

    def run(self) -> None:
        """Start the enhanced voice-controlled shell"""
        print("🎤 Starting Enhanced Voice-Controlled Mini Bash...")
        print("Press Ctrl+C to exit")
        
        try:
            # Start shell
            if not self.start_shell():
                return
            
            # Start voice processing
            self.process_voice_command()
            
        except KeyboardInterrupt:
            print("\n👋 Voice control stopped!")
        finally:
            # Cleanup
            self.stop_shell()

def main():
    """Main entry point"""
    print("🔥 Advanced Mini Bash - Enhanced Voice Control (Phase 3)")
    print("=" * 70)
    
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
    
    # Start enhanced voice control
    voice_shell = EnhancedVoiceShell()
    voice_shell.run()

if __name__ == "__main__":
    main()
