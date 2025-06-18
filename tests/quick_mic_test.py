#!/usr/bin/env python3
"""
Quick microphone test - just check if mic is working
"""

import sys
import os
import time

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from speech_recognizer import AstroSpeechRecognizer

print("🎤 QUICK MICROPHONE TEST")
print("=" * 40)

recognizer = AstroSpeechRecognizer()

print("📦 Loading model...")
if not recognizer.load_model():
    print("❌ Model failed")
    exit(1)

print("🎧 Setting up microphone...")
if not recognizer.setup_audio():
    print("❌ Microphone failed")
    exit(1)

print("\n✅ Microphone is working!")
print("🎤 Say something in 3 seconds...")

time.sleep(3)
print("🔴 Recording 5 seconds...")

audio_data = recognizer.record_audio_chunk()
if audio_data:
    print("✅ Audio recorded!")
    print("🧠 Transcribing...")
    
    text = recognizer.transcribe_audio(audio_data)
    if text:
        print(f"🎯 I heard: '{text}'")
        
        if 'astro' in text:
            print("🚀 Wake word detected!")
        else:
            print("💡 Try saying 'Astro' next time")
    else:
        print("❌ No speech detected")
else:
    print("❌ No audio recorded")

recognizer.stop_listening()
print("✅ Test complete!")