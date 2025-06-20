#!/usr/bin/env python3
"""
🎤 SEQUENTIAL ASTRO VOICE CONTROLLER
Sequential voice control for Gaia Sky - no feedback loops or async overlaps
Each operation blocks until completion for reliable voice interaction
"""

import sys
import os
import time

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from utils.config import setup_project_path, setup_logger
from remote_controller import SpaceNavigationController
from tts_engine import CoquiTTSEngine
from speech_recognizer import UniversalSpeechRecognizer
from sequential_voice_controller import SequentialVoiceController

# Setup project path and logging
setup_project_path()
logger = setup_logger(__name__)

def main():
    """Sequential voice controller for hands-free space exploration"""
    
    print("🎤 SEQUENTIAL ASTRO VOICE CONTROLLER")
    print("=" * 55)
    print("🚀 Pure sequential voice control for Gaia Sky")
    print("🎧 No feedback loops - one operation at a time!")
    print("🎯 Reliable voice commands with completion tracking")
    print("=" * 55)
    
    # Initialize components
    print("🔄 Initializing voice control components...")
    
    # Initialize space navigation controller
    space_controller = SpaceNavigationController()
    
    # Initialize TTS engine
    print("🗣️ Loading neural TTS engine...")
    tts_engine = CoquiTTSEngine()
    
    # Initialize speech recognizer
    print("🎤 Setting up speech recognition...")
    speech_recognizer = UniversalSpeechRecognizer()
    
    # Connect to Gaia Sky
    print("🔌 Connecting to Gaia Sky...")
    if not space_controller.connect():
        print("❌ Failed to connect to Gaia Sky")
        print("💡 Make sure Gaia Sky is running with Python bridge enabled")
        return
    
    print("✅ Connected to Gaia Sky!")
    
    # Wait for TTS to be ready
    print("⏳ Waiting for TTS engine to load...")
    for i in range(100):  # Wait up to 10 seconds
        if tts_engine.is_ready():
            print("✅ TTS engine ready!")
            break
        if i % 10 == 0:
            print(f"   Loading... {i//10 + 1}/10")
        time.sleep(0.1)
    
    if not tts_engine.is_ready():
        print("⚠️ TTS engine still loading, continuing anyway...")
    
    # Create sequential voice controller
    print("🎛️ Setting up sequential voice control...")
    
    def command_executor(command: str) -> str:
        """Execute commands using the space controller"""
        return space_controller.execute_command_with_completion(command)
    
    voice_controller = SequentialVoiceController(
        tts_engine=tts_engine,
        speech_recognizer=speech_recognizer,
        command_executor=command_executor
    )
    
    print("\n🎯 SEQUENTIAL VOICE CONTROL READY!")
    print("\n💡 HOW IT WORKS:")
    print("  1️⃣ System speaks → waits for completion")
    print("  2️⃣ Listens for your command → waits for command")
    print("  3️⃣ Processes command → waits for execution")
    print("  4️⃣ Gives feedback → waits for completion")
    print("  5️⃣ Repeats cycle")
    
    print("\n🗣️ EXAMPLE COMMANDS:")
    print("  • 'Take me to Mars'")
    print("  • 'Go to Jupiter'")
    print("  • 'Take a screenshot'")
    print("  • 'Land on the Moon'")
    
    print("\n🔍 INDICATORS:")
    print("  🟢 READY - Listening for command")
    print("  🔴 PROCESSING - Analyzing speech")
    print("  ⚡ EXECUTING - Running on Gaia Sky")
    print("  📢 FEEDBACK - Giving result")
    
    print("\n🛑 Press Ctrl+C to stop")
    print("=" * 55)
    
    try:
        # Start the sequential voice control loop
        voice_controller.run_voice_control_loop()
        
    except KeyboardInterrupt:
        print("\n🛑 Voice control stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Voice control error: {e}")
    finally:
        print("🔌 Disconnecting from Gaia Sky...")
        voice_controller.stop()
        space_controller.disconnect()
        print("👋 Goodbye! Thanks for exploring the universe with Sequential Astro!")

if __name__ == "__main__":
    main()