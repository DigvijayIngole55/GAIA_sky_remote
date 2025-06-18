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
    
    # Initialize controller
    controller = SpaceNavigationController()
    
    # Connect to Gaia Sky
    print("🔌 Connecting to Gaia Sky...")
    if not controller.connect():
        print("❌ Failed to connect to Gaia Sky")
        print("💡 Make sure Gaia Sky is running with Python bridge enabled")
        return
    
    print("✅ Connected to Gaia Sky!")
    
    # Start speech recognition
    print("🎤 Starting voice recognition...")
    if not controller.start_speech_recognition():
        print("❌ Failed to start speech recognition")
        print("💡 Make sure microphone is connected and working")
        print("💡 Install dependencies: pip install openai-whisper pyaudio")
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
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Voice control stopped by user")
    
    finally:
        print("🔌 Disconnecting...")
        controller.disconnect()
        print("👋 Goodbye! Thanks for exploring the universe with Astro!")

if __name__ == "__main__":
    main()