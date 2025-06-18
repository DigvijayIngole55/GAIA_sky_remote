#!/usr/bin/env python3
"""
DEBUG VOICE CONTROLLER
Debug version to trace exactly what's happening with voice capture
"""

import sys
import os
import time
import threading

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.config import setup_project_path, setup_logger
from remote_controller import SpaceNavigationController

# Setup project path and logging
setup_project_path()
logger = setup_logger(__name__)
from speech_recognizer import UniversalSpeechRecognizer

def debug_voice_recognition():
    """Debug the voice recognition flow step by step"""
    
    print("🐛 DEBUG VOICE CONTROLLER")
    print("=" * 50)
    
    # Initialize components separately for debugging
    print("1️⃣ Testing Speech Recognizer...")
    recognizer = UniversalSpeechRecognizer()
    
    # Check model loading
    print("   Loading Whisper model...")
    if recognizer.load_model():
        print("   ✅ Model loaded successfully")
    else:
        print("   ❌ Model loading failed")
        return
    
    # Check audio setup
    print("   Setting up audio...")
    if recognizer.setup_audio():
        print("   ✅ Audio setup successful")
    else:
        print("   ❌ Audio setup failed")
        return
    
    # Test callback function
    commands_received = []
    
    def debug_callback(command: str):
        """Debug callback to track commands"""
        print(f"   🎤 CALLBACK TRIGGERED: '{command}'")
        commands_received.append(command)
    
    print("\n2️⃣ Testing Voice Capture...")
    print("   Starting listening with debug callback...")
    
    if recognizer.start_listening(debug_callback):
        print("   ✅ Listening started")
        print("\n   🎤 SPEAK NOW! Say 'take me to mars' clearly...")
        print("   🗣️ Try these commands:")
        print("     - 'take me to mars'")
        print("     - 'go to jupiter'")
        print("     - 'take screenshot'")
        print("   Listening for 15 seconds...")
        
        # Monitor for 15 seconds with better feedback
        start_time = time.time()
        last_feedback = 0
        while time.time() - start_time < 15:
            if commands_received:
                print(f"\n   ✅ Command received: {commands_received[-1]}")
                break
            
            # Give feedback every 3 seconds
            elapsed = time.time() - start_time
            if elapsed - last_feedback >= 3:
                remaining = 15 - elapsed
                print(f"\n   ⏱️ {remaining:.0f} seconds remaining... Keep speaking!")
                last_feedback = elapsed
            
            time.sleep(0.5)
            print(".", end="", flush=True)
        
        print("\n")
        
        recognizer.stop_listening()
        
        if commands_received:
            print(f"✅ SUCCESS: Captured {len(commands_received)} commands")
            for i, cmd in enumerate(commands_received):
                print(f"   Command {i+1}: '{cmd}'")
        else:
            print("❌ NO COMMANDS CAPTURED")
            print("💡 Possible issues:")
            print("   - Microphone permission denied")
            print("   - Microphone not working")
            print("   - Speech too quiet/unclear")
            print("   - Background noise interference")
            print("\n💡 Try:")
            print("   - Check System Preferences > Security & Privacy > Microphone")
            print("   - Speak louder and clearer")
            print("   - Move closer to microphone")
    else:
        print("   ❌ Failed to start listening")
    
    print("\n3️⃣ Testing Full Integration...")
    controller = SpaceNavigationController()
    
    if controller.connect():
        print("   ✅ Connected to Gaia Sky")
        
        # Test execute_command directly
        print("   Testing command execution...")
        result = controller.execute_command("take me to mars")
        print(f"   Command result: {result}")
        
        controller.disconnect()
    else:
        print("   ❌ Failed to connect to Gaia Sky")
    
    print("\n" + "=" * 50)
    print("🐛 DEBUG COMPLETE")

if __name__ == "__main__":
    debug_voice_recognition()