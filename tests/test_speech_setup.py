#!/usr/bin/env python3
"""
Test script to verify speech recognition setup
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

def test_dependencies():
    """Test if required dependencies are available"""
    
    print("🧪 Testing Speech Recognition Dependencies")
    print("=" * 50)
    
    # Test whisper
    try:
        import whisper
        print("✅ OpenAI Whisper: Available")
        
        # Test model loading
        print("📦 Loading Whisper Base model...")
        model = whisper.load_model("base")
        print("✅ Whisper Base model: Loaded successfully")
        
    except ImportError:
        print("❌ OpenAI Whisper: Not installed")
        print("💡 Install with: pip install openai-whisper")
        return False
    except Exception as e:
        print(f"❌ Whisper model loading failed: {e}")
        return False
    
    # Test pyaudio
    try:
        import pyaudio
        print("✅ PyAudio: Available")
        
        # Test audio system
        audio = pyaudio.PyAudio()
        print("✅ Audio system: Initialized")
        audio.terminate()
        
    except ImportError:
        print("❌ PyAudio: Not installed")
        print("💡 Install with: pip install pyaudio")
        return False
    except Exception as e:
        print(f"❌ Audio system failed: {e}")
        return False
    
    print("=" * 50)
    print("✅ All dependencies ready for speech recognition!")
    return True

def test_speech_recognizer():
    """Test the speech recognizer class"""
    
    print("\n🎤 Testing Astro Speech Recognizer")
    print("=" * 50)
    
    try:
        from speech_recognizer import AstroSpeechRecognizer
        
        recognizer = AstroSpeechRecognizer()
        print("✅ AstroSpeechRecognizer: Created")
        
        # Test model loading
        if recognizer.load_model():
            print("✅ Model loading: Success")
        else:
            print("❌ Model loading: Failed")
            return False
        
        # Test audio setup
        if recognizer.setup_audio():
            print("✅ Audio setup: Success")
            recognizer.stop_listening()  # Cleanup
        else:
            print("❌ Audio setup: Failed")
            return False
        
        print("=" * 50)
        print("✅ Speech recognizer fully functional!")
        return True
        
    except Exception as e:
        print(f"❌ Speech recognizer test failed: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 ASTRO SPEECH RECOGNITION SETUP TEST")
    print("Testing system readiness for voice control")
    print("\n")
    
    # Test dependencies
    if not test_dependencies():
        print("\n❌ SETUP INCOMPLETE")
        print("Install missing dependencies and try again")
        return
    
    # Test speech recognizer
    if not test_speech_recognizer():
        print("\n❌ SPEECH RECOGNIZER FAILED")
        print("Check microphone and audio permissions")
        return
    
    print("\n🎯 SETUP COMPLETE!")
    print("✅ Ready for voice-controlled space exploration!")
    print("🚀 Run: python voice_controller.py")

if __name__ == "__main__":
    main()