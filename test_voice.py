#!/usr/bin/env python3
"""
Test script for voice control module
This script tests the voice control functionality without requiring actual voice input
"""

import os
import sys
import json
import time

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from google.cloud import speech
        print("✅ Google Cloud Speech imported")
    except ImportError as e:
        print(f"❌ Google Cloud Speech import failed: {e}")
        return False
    
    try:
        from google.cloud import translate_v2 as translate
        print("✅ Google Cloud Translation imported")
    except ImportError as e:
        print(f"❌ Google Cloud Translation import failed: {e}")
        return False
    
    try:
        from google.cloud import texttospeech
        print("✅ Google Cloud Text-to-Speech imported")
    except ImportError as e:
        print(f"❌ Google Cloud Text-to-Speech import failed: {e}")
        return False
    
    try:
        import pyaudio
        print("✅ PyAudio imported")
    except ImportError as e:
        print(f"❌ PyAudio import failed: {e}")
        return False
    
    try:
        import wave
        print("✅ Wave imported")
    except ImportError as e:
        print(f"❌ Wave import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration files"""
    print("\n🔍 Testing configuration...")
    
    # Test voice_config.json
    if os.path.exists("voice_config.json"):
        try:
            with open("voice_config.json", 'r') as f:
                config = json.load(f)
            print("✅ voice_config.json loaded successfully")
        except Exception as e:
            print(f"❌ voice_config.json error: {e}")
            return False
    else:
        print("⚠️  voice_config.json not found (will be created)")
    
    # Test hindi_commands.json
    if os.path.exists("hindi_commands.json"):
        try:
            with open("hindi_commands.json", 'r', encoding='utf-8') as f:
                commands = json.load(f)
            print("✅ hindi_commands.json loaded successfully")
        except Exception as e:
            print(f"❌ hindi_commands.json error: {e}")
            return False
    else:
        print("⚠️  hindi_commands.json not found (will be created)")
    
    return True

def test_credentials():
    """Test Google Cloud credentials"""
    print("\n🔍 Testing Google Cloud credentials...")
    
    if not os.path.exists("credentials.json"):
        print("❌ credentials.json not found!")
        print("   Please download your Google Cloud credentials and place them as 'credentials.json'")
        return False
    
    try:
        with open("credentials.json", 'r') as f:
            creds = json.load(f)
        
        required_fields = ["type", "project_id", "private_key", "client_email"]
        for field in required_fields:
            if field not in creds:
                print(f"❌ Missing field in credentials: {field}")
                return False
        
        print("✅ credentials.json is valid")
        return True
        
    except Exception as e:
        print(f"❌ credentials.json error: {e}")
        return False

def test_mini_bash():
    """Test if Mini Bash is available"""
    print("\n🔍 Testing Mini Bash...")
    
    if not os.path.exists("./mini-bash"):
        print("❌ mini-bash executable not found!")
        print("   Please run 'make' first to build the shell")
        return False
    
    if not os.access("./mini-bash", os.X_OK):
        print("❌ mini-bash is not executable!")
        print("   Please run 'chmod +x mini-bash'")
        return False
    
    print("✅ mini-bash executable found")
    return True

def test_voice_module():
    """Test voice module initialization"""
    print("\n🔍 Testing voice module initialization...")
    
    try:
        # Set environment variable for credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
        
        # Test shell bridge
        from shell_bridge import ShellBridge, VoiceCommandProcessor
        print("✅ Shell bridge imported")
        
        # Test voice module
        from voice_module import VoiceControlledShell
        print("✅ Voice module imported")
        
        # Test enhanced voice module
        from voice_enhanced import EnhancedVoiceShell
        print("✅ Enhanced voice module imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Voice module import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Voice module error: {e}")
        return False

def test_audio_system():
    """Test audio system"""
    print("\n🔍 Testing audio system...")
    
    try:
        import pyaudio
        
        audio = pyaudio.PyAudio()
        device_count = audio.get_device_count()
        
        if device_count == 0:
            print("❌ No audio devices found!")
            return False
        
        print(f"✅ Found {device_count} audio devices")
        
        # Test default input device
        try:
            default_input = audio.get_default_input_device_info()
            print(f"✅ Default input device: {default_input['name']}")
        except Exception as e:
            print(f"⚠️  Default input device error: {e}")
        
        audio.terminate()
        return True
        
    except Exception as e:
        print(f"❌ Audio system error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Advanced Mini Bash - Voice Control Test Suite")
    print("=" * 55)
    
    tests = [
        ("Import Test", test_imports),
        ("Config Test", test_config),
        ("Credentials Test", test_credentials),
        ("Mini Bash Test", test_mini_bash),
        ("Voice Module Test", test_voice_module),
        ("Audio System Test", test_audio_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "="*55)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Voice control is ready to use!")
        print("\n🚀 Next steps:")
        print("   1. Run: python3 voice_demo.py")
        print("   2. Or: python3 voice_enhanced.py")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\n🔧 Common fixes:")
        print("   • Install dependencies: pip3 install -r requirements.txt")
        print("   • Get Google Cloud credentials")
        print("   • Build Mini Bash: make clean && make")
        return False

def main():
    """Main test function"""
    success = run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
