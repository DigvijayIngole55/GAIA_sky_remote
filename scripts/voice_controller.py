#!/usr/bin/env python3
"""
🎤 ASTRO VOICE CONTROLLER
Pure voice control for Gaia Sky space navigation
Direct commands - no wake word needed!
"""

import sys
import os
import time

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from utils.config import setup_project_path, setup_logger
from remote_controller import SpaceNavigationController
from tts_engine import CoquiTTSEngine

# Setup project path and logging
setup_project_path()
logger = setup_logger(__name__)

def main():
    """Voice-only controller for hands-free space exploration"""
    
    print("🎤 ASTRO VOICE CONTROLLER")
    print("=" * 50)
    print("🚀 Pure voice control for Gaia Sky")
    print("🎧 Hands-free space exploration!")
    print("🎯 Direct commands - no wake word needed!")
    print("=" * 50)
    
    # Initialize controller and TTS
    controller = SpaceNavigationController()
    print("🔄 Initializing neural voice system...")
    tts = CoquiTTSEngine()
    
    # Connect to Gaia Sky
    print("🔌 Connecting to Gaia Sky...")
    # Wait for TTS to be ready before speaking
    if tts.is_ready():
        tts.speak_indicator_sync("connecting")
    else:
        print("   (Voice system loading in background...)")
    
    if not controller.connect():
        print("❌ Failed to connect to Gaia Sky")
        print("💡 Make sure Gaia Sky is running with Python bridge enabled")
        tts.speak_indicator_sync("failed")
        return
    
    print("✅ Connected to Gaia Sky!")
    # Ensure TTS is ready before speaking - use SYNCHRONOUS speaking to avoid feedback
    if tts.is_ready():
        tts.speak_indicator_sync("connected")  # Blocks until complete
    else:
        print("   (Waiting for voice system to load...)")
        # Wait up to 10 seconds for TTS to be ready
        import time
        for _ in range(100):
            if tts.is_ready():
                tts.speak_indicator_sync("connected")  # Blocks until complete
                break
            time.sleep(0.1)
    
    # Start speech recognition with shared TTS engine
    print("🎤 Starting voice recognition...")
    # Pass the TTS engine to avoid duplicate initialization
    controller.tts_engine = tts
    if not controller.start_speech_recognition():
        print("❌ Failed to start speech recognition")
        print("💡 Make sure microphone is connected and working")
        print("💡 Install dependencies: pip install openai-whisper pyaudio")
        tts.speak_indicator_sync("failed")
        controller.disconnect()
        return
    
    print("\n" + "🎯 VOICE CONTROL ACTIVE!" + "\n")
    print("💡 QUICK COMMANDS:")
    print("  🗣️ 'Take me to Mars'")
    print("  🗣️ 'Go to Jupiter'") 
    print("  🗣️ 'Take a screenshot'")
    print("  🗣️ 'Land on the Moon'")
    print("\n🔍 INDICATORS:")
    print("  🟢 READY - System ready for your command")
    print("  🔴 PROCESSING - Analyzing your speech")
    print("  🎤 Heard - Command captured successfully")
    
    print("\n🛑 Press Ctrl+C to stop voice control")
    print("=" * 50)
    
    # Initial ready indicator - ensure TTS is ready
    print("🔄 Preparing voice system for commands...")
    if tts.is_ready():
        tts.speak_indicator_sync("ready")  # Blocks until complete
    else:
        print("   (Waiting for neural voice system...)")
        # Wait up to 15 seconds for TTS to be ready
        for i in range(150):
            if tts.is_ready():
                print("   ✅ Voice system ready!")
                tts.speak_indicator_sync("ready")  # Blocks until complete
                break
            if i % 10 == 0:  # Print progress every second
                print(f"   Loading... {i//10 + 1}/15")
            time.sleep(0.1)
        
        if not tts.is_ready():
            print("   ⚠️ Voice system still loading, continuing without audio cues")
    
    print("\n🟢 SYSTEM ACTIVE - Listening for voice commands...")
    print("🎤 Speak clearly: 'Take me to Mars', 'Go to Jupiter', 'Take screenshot'")
    
    try:
        # Keep running until interrupted
        ready_counter = 0
        while True:
            time.sleep(1)
            ready_counter += 1
            
            # Periodic ready indicator every 60 seconds (less frequent)
            if ready_counter >= 60 and tts.is_ready():
                tts.speak_indicator_sync("ready")
                ready_counter = 0
            
    except KeyboardInterrupt:
        print("\n🛑 Voice control stopped by user")
    
    finally:
        print("🔌 Disconnecting...")
        controller.disconnect()
        print("👋 Goodbye! Thanks for exploring the universe with Astro!")

if __name__ == "__main__":
    main()