#!/usr/bin/env python3
"""Test command mapping functionality"""

import sys
sys.path.insert(0, '.')

from shell_bridge import VoiceCommandProcessor, ShellBridge

# Create instances
shell_bridge = ShellBridge()
processor = VoiceCommandProcessor(shell_bridge)

print("🧪 Testing Command Mapping")
print("=" * 60)

# Test cases
test_cases = [
    ("लिस्ट फाइल्स!", "hindi"),
    ("List files!", "english"),
    ("होल्डर खोलो!", "hindi"),
    ("फोल्डर खोलो", "hindi"),
    ("current directory", "english"),
    ("वर्तमान फोल्डर", "hindi"),
    ("list files", "english"),
    ("show files", "english"),
]

for voice_text, language in test_cases:
    mapped = processor.map_command(voice_text, language)
    print(f"📝 '{voice_text}' ({language}) → '{mapped}'")
    
print("\n" + "=" * 60)
print("✅ Command mapping test complete!")

# Close shell bridge
shell_bridge.stop_shell()

