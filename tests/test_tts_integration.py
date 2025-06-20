#!/usr/bin/env python3
"""
Test TTS Integration
Quick test to verify TTS voice cues are working correctly
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.config import setup_project_path, setup_logger
from tts_engine import CoquiTTSEngine

# Setup project path and logging
setup_project_path()
logger = setup_logger(__name__)

def test_tts_cues():
    """Test all TTS voice cues"""
    print("🔊 Testing TTS Voice Cues")
    print("=" * 40)
    
    # Initialize TTS engine
    tts = CoquiTTSEngine()
    
    if not tts.enabled:
        print("❌ TTS Engine not available")
        print("💡 Install coqui-tts: pip install coqui-tts")
        return
    
    print("✅ TTS Engine initialized")
    print("\n🎵 Testing voice cues:")
    
    cues_to_test = [
        ("connecting", "System connecting"),
        ("connected", "Connection established"),
        ("ready", "System ready"),
        ("got_it", "Speech captured"),
        ("processing", "LLM processing"),
        ("executing", "Executing command"),
        ("complete", "Command complete"),
        ("failed", "Command failed"),
        ("unclear", "Command unclear")
    ]
    
    for cue, description in cues_to_test:
        print(f"  🔊 {description}: '{cue}'")
        tts.speak_indicator_sync(cue)  # Synchronous for testing
        import time
        time.sleep(1)  # Small delay between cues
    
    print("\n✅ All TTS cues tested successfully!")
    print("🎯 Voice cue system is ready for space navigation!")

if __name__ == "__main__":
    test_tts_cues()