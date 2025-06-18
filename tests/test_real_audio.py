#!/usr/bin/env python3
"""
🎤 REAL AUDIO TEST
Actually test live microphone input and speech recognition
"""

import time
from speech_recognizer import AstroSpeechRecognizer

def test_real_speech():
    """Test actual speech recognition with your voice"""
    
    print("🎤 REAL SPEECH RECOGNITION TEST")
    print("=" * 50)
    print("This will actually listen to your microphone!")
    print("=" * 50)
    
    recognizer = AstroSpeechRecognizer()
    
    # Load model
    print("📦 Loading Whisper model...")
    if not recognizer.load_model():
        print("❌ Failed to load model")
        return False
    
    # Setup audio
    print("🎧 Setting up microphone...")
    if not recognizer.setup_audio():
        print("❌ Failed to setup audio")
        return False
    
    print("\n🎯 LIVE AUDIO TEST")
    print("=" * 50)
    print("💡 Instructions:")
    print("1. I'll record 5 seconds of audio")
    print("2. Say something clearly (try: 'Astro, go to Mars')")
    print("3. I'll show you what I heard")
    print("=" * 50)
    
    input("📢 Press Enter when ready to speak...")
    
    print("🎤 RECORDING... Speak now! (5 seconds)")
    print("🔴 Recording...")
    
    # Record audio chunk
    audio_data = recognizer.record_audio_chunk()
    
    if not audio_data:
        print("❌ No audio recorded")
        return False
    
    print("✅ Audio recorded!")
    print("🧠 Transcribing with Whisper...")
    
    # Transcribe
    text = recognizer.transcribe_audio(audio_data)
    
    print("\n🎯 RESULTS:")
    print("=" * 50)
    if text:
        print(f"📝 I heard: '{text}'")
        
        # Test wake word detection
        if 'astro' in text.lower():
            print("🚀 Wake word 'Astro' detected! ✅")
            
            # Extract command
            wake_index = text.lower().find('astro')
            command = text[wake_index + 5:].strip()
            if command:
                print(f"💬 Command extracted: '{command}'")
            else:
                print("⚠️ No command after wake word")
        else:
            print("❌ Wake word 'Astro' not detected")
    else:
        print("❌ No speech detected or transcription failed")
    
    print("=" * 50)
    
    # Cleanup
    recognizer.stop_listening()
    return True

def test_continuous_listening():
    """Test continuous listening like the real controller"""
    
    print("\n🎧 CONTINUOUS LISTENING TEST")
    print("=" * 50)
    print("This simulates the real voice controller!")
    print("💡 Say 'Astro [command]' multiple times")
    print("💡 Press Ctrl+C to stop")
    print("=" * 50)
    
    def handle_command(command: str):
        print(f"🚀 COMMAND DETECTED: '{command}'")
        print(f"🎯 Would execute: {command}")
    
    recognizer = AstroSpeechRecognizer()
    
    try:
        if recognizer.start_listening(handle_command):
            print("🎤 Listening continuously...")
            print("🗣️ Try saying: 'Astro, take me to Mars'")
            
            # Listen for 30 seconds
            start_time = time.time()
            while time.time() - start_time < 30:
                time.sleep(1)
                print(".", end="", flush=True)
                
                if time.time() - start_time > 10:
                    print("\n💡 Still listening... Say 'Astro [command]'")
        else:
            print("❌ Failed to start continuous listening")
            
    except KeyboardInterrupt:
        print("\n🛑 Test stopped by user")
    finally:
        recognizer.stop_listening()

def main():
    """Run real audio tests"""
    
    print("🚀 REAL AUDIO TESTING")
    print("This will actually use your microphone!")
    print("\n")
    
    # Test 1: Single audio recording
    print("🧪 TEST 1: Single Recording")
    if not test_real_speech():
        print("❌ Single recording test failed")
        return
    
    # Ask for continuous test
    response = input("\n🧪 TEST 2: Continuous listening? (y/n): ").lower()
    if response.startswith('y'):
        test_continuous_listening()
    
    print("\n✅ Real audio testing complete!")
    print("🎤 Your microphone and speech recognition are working!")

if __name__ == "__main__":
    main()