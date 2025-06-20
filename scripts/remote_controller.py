#!/usr/bin/env python3
"""
🚀 ASTRO REMOTE CONTROLLER - MAIN ENTRY POINT
Enhanced command-line interface with multiple control modes
"""

import sys
import os
import time

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from utils.config import setup_project_path, setup_logger
from remote_controller import SpaceNavigationController, SPEECH_AVAILABLE
from tts_engine import UniversalTTSEngine

# Setup project path and logging
setup_project_path()
logger = setup_logger(__name__)

def show_help():
    """Display extensive command examples"""
    print("🌟 EXTENSIVE COMMAND EXAMPLES:")
    print("=" * 60)
    
    print("\n🚀 NAVIGATION COMMANDS:")
    print("  • go to mars              • take me to jupiter")
    print("  • fly to saturn           • travel to the sun")
    print("  • navigate to venus       • visit earth")
    print("  • head to mercury         • let's go to neptune")
    print("  • show me pluto           • bring me to uranus")
    print("  • find the iss            • locate alpha centauri")

    print("\n🛬 LANDING COMMANDS:")
    print("  • land on the moon        • land on mars")
    print("  • touch down on europa    • set down on titan")
    print("  • descend to earth        • land at the red planet")

    print("\n👁️ TRACKING COMMANDS:")
    print("  • track saturn            • follow jupiter")
    print("  • keep an eye on mars     • watch the moon")
    print("  • focus on venus          • track hubble telescope")

    print("\n🔍 EXPLORATION COMMANDS:")
    print("  • explore venus           • investigate mars")
    print("  • examine jupiter         • study saturn")
    print("  • discover neptune        • check out the sun")

    print("\n📸 PHOTO COMMANDS:")
    print("  • take a screenshot       • capture image")
    print("  • take a photo            • snap a picture")
    print("  • save this view")

    print("\n🌌 CELESTIAL OBJECT ALIASES:")
    print("  • red planet → Mars       • blue planet → Earth")
    print("  • gas giant → Jupiter     • ringed planet → Saturn")
    print("  • our star → Sun          • morning star → Venus")
    print("  • evening star → Venus    • luna → Moon")
    print("  • space station → ISS     • nearest star → Alpha Centauri")

    print("\n⭐ STARS & DEEP SPACE:")
    print("  • go to alpha centauri    • visit betelgeuse")
    print("  • explore vega            • navigate to sirius")

    print("\n🛰️ SPACECRAFT:")
    print("  • find the iss            • track hubble telescope")

    print("\n🆘 RECOVERY COMMANDS (when stuck):")
    print("  • free camera             • unlock camera")
    print("  • release camera          • get unstuck")
    print("  • stop camera             • back to space")
    print("  • return to space")

    print("\n🎬 MULTI-TOOL COMMANDS (Cool Features!):")
    print("  • tour the solar system   • grand tour of planets")
    print("  • tour inner planets      • tour gas giants")
    print("  • cinematic journey to mars")
    print("  • stream tour of jupiter moons")
    print("  • stream tour of saturn rings")
    print("  • visit mars then land on it")
    print("  • go to jupiter and track it")

    print("\n🌟 ADVANCED SEQUENCES:")
    print("  📺 Stream Tours    - Live commentary with multiple stops")
    print("  🎬 Cinematic       - Movie-like sequences with effects")
    print("  🗺️ Grand Tours     - Multi-planet expeditions")
    print("  🔄 Multi-Step      - Chain multiple commands together")

    print("\n" + "=" * 60)
    print("💡 The controller now supports MULTI-TOOL sequences!")
    print("   Single tools: 'go to Mars' | Multi-tools: 'tour the solar system'")
    print("🆘 If you get stuck after landing, try: 'free camera' or 'back to space'")
    print("🎬 Try advanced commands for epic space exploration experiences!\n")

def hands_free_mode(controller):
    """Pure hands-free voice control mode"""
    if not SPEECH_AVAILABLE:
        print("❌ Speech recognition not available")
        print("💡 Install with: pip install openai-whisper pyaudio")
        return
    
    print("🎧 Starting hands-free voice control...")
    print("💡 Say commands directly to control Gaia Sky")
    print("💡 Example: 'Take me to Mars'")
    print("🛑 Press Ctrl+C to exit")
    print("=" * 50)
    
    def handle_voice_command(command: str):
        """Handle voice commands and execute them"""
        print(f"\n🎤 Voice Command: '{command}'")
        result = controller.execute_command(command)
        print(f"🚀 Result: {result}\n")
        print("🎧 Listening for next command...")
    
    try:
        # Start speech recognition with our custom callback
        if controller.start_speech_recognition(handle_voice_command):
            # Keep running until interrupted
            while True:
                time.sleep(1)
        else:
            print("❌ Failed to start speech recognition")
            
    except KeyboardInterrupt:
        print("\n🛑 Voice control stopped")
    finally:
        controller.stop_speech_recognition()
        controller.disconnect()

def text_mode(controller):
    """Text-only command mode"""
    show_help()
    
    try:
        while True:
            user_input = input("🌌 Command: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            if user_input.lower() in ['help', 'h', '?']:
                show_help()
                continue
                
            if not user_input:
                continue
                
            print(f"⚡ Processing: {user_input}")
            result = controller.execute_command(user_input)
            print(f"🎯 {result}\n")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        controller.disconnect()

def mixed_mode(controller):
    """Mixed text and voice mode"""
    show_help()
    print("\n💡 Type 'speech' to activate voice control")
    print("💡 Type 'stop speech' to disable voice control")
    
    try:
        while True:
            user_input = input("🌌 Command: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            if user_input.lower() in ['help', 'h', '?']:
                show_help()
                continue
            
            if user_input.lower() in ['speech', 'voice', 'listen']:
                if not SPEECH_AVAILABLE:
                    print("❌ Speech recognition not available")
                    print("💡 Install with: pip install openai-whisper pyaudio")
                    continue
                    
                print("🎤 Starting speech recognition...")
                if controller.start_speech_recognition():
                    print("🎧 Speech recognition is now active!")
                    print("💡 Say commands directly to control Gaia Sky")
                    print("💡 Press Enter to stop speech recognition")
                    input()  # Wait for user to press Enter
                    controller.stop_speech_recognition()
                continue
            
            if user_input.lower() == 'stop speech':
                controller.stop_speech_recognition()
                continue
                
            if not user_input:
                continue
                
            print(f"⚡ Processing: {user_input}")
            result = controller.execute_command(user_input)
            print(f"🎯 {result}\n")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        controller.disconnect()

def main():
    """Enhanced command-line interface with speech recognition"""
    print("🚀 Standalone Gaia Sky Remote Controller")
    print("Natural language commands with extensive vocabulary support!")
    print("🎤 Direct voice control - no wake word needed!")
    print("=" * 60)
    
    controller = SpaceNavigationController()
    tts = UniversalTTSEngine()
    
    # Connect to Gaia Sky first
    print("🔌 Connecting to Gaia Sky...")
    if not controller.connect():
        print("❌ Failed to connect to Gaia Sky. Make sure it's running with Python bridge enabled.")
        return
        
    print("✅ Connected to Gaia Sky!")
    
    # Mode selection
    print("\n🎯 SELECT CONTROL MODE:")
    print("=" * 30)
    print("1️⃣  Hands-Free Voice Control")
    print("2️⃣  Text Commands") 
    print("3️⃣  Mixed Mode (Text + Voice)")
    print("=" * 30)
    
    while True:
        try:
            choice = input("👆 Choose mode (1/2/3): ").strip()
            
            if choice == "1":
                # Hands-free voice mode
                print("\n🎤 HANDS-FREE VOICE MODE")
                hands_free_mode(controller)
                break
            elif choice == "2":
                # Text-only mode
                print("\n⌨️ TEXT COMMAND MODE")
                text_mode(controller)
                break
            elif choice == "3":
                # Mixed mode
                print("\n🔀 MIXED MODE")
                mixed_mode(controller)
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            controller.disconnect()
            return

if __name__ == "__main__":
    main()