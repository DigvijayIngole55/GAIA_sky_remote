#!/usr/bin/env python3
"""
🎤 ASTRO SPEECH RECOGNIZER
Lightweight speech recognition using OpenAI Whisper
Optimized for direct space navigation commands (no wake word needed)
"""

import whisper
import pyaudio
import threading
import time
from typing import Optional, Callable
import logging
import numpy as np

try:
    from .utils.config import (
        WHISPER_MODEL_SIZE, SAMPLE_RATE, CHUNK_DURATION, 
        MIN_SPEECH_LENGTH, AUDIO_CHANNELS, AUDIO_FRAMES_PER_BUFFER
    )
except ImportError:
    # Fallback for direct execution
    from utils.config import (
        WHISPER_MODEL_SIZE, SAMPLE_RATE, CHUNK_DURATION, 
        MIN_SPEECH_LENGTH, AUDIO_CHANNELS, AUDIO_FRAMES_PER_BUFFER
    )

# Configure logging
logger = logging.getLogger(__name__)

class UniversalSpeechRecognizer:
    """
    Lightweight speech recognizer for Astro space navigation
    Uses Whisper Base model for balanced accuracy and performance
    Processes direct commands without wake words
    """
    
    def __init__(self, 
                 model_size: str = WHISPER_MODEL_SIZE,
                 sample_rate: int = SAMPLE_RATE,
                 chunk_duration: float = CHUNK_DURATION,
                 min_speech_length: int = MIN_SPEECH_LENGTH):
        """
        Initialize speech recognizer for direct commands
        
        Args:
            model_size: Whisper model size (tiny/base/small/medium/large)
            sample_rate: Audio sample rate in Hz
            chunk_duration: Audio chunk duration in seconds
            min_speech_length: Minimum words required to process command
        """
        self.model_size = model_size
        self.min_speech_length = min_speech_length
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_size = int(sample_rate * chunk_duration)
        
        # Audio settings
        self.format = pyaudio.paInt16
        self.channels = AUDIO_CHANNELS
        
        # State
        self.is_listening = False
        self.audio = None
        self.stream = None
        self.model = None
        self.command_callback = None
        
        logger.info("🎤 Astro Speech Recognizer initialized for direct commands")
    
    def load_model(self) -> bool:
        """Load Whisper model"""
        try:
            logger.info(f"Loading Whisper {self.model_size.title()} model...")
            self.model = whisper.load_model(self.model_size)
            logger.info("✅ Whisper model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load Whisper model: {e}")
            return False
    
    def setup_audio(self) -> bool:
        """Initialize audio recording with device detection"""
        try:
            self.audio = pyaudio.PyAudio()
            
            # Check for available input devices
            info = self.audio.get_host_api_info_by_index(0)
            logger.info(f"🎤 Audio Host: {info.get('name')}")
            
            # List input devices
            input_devices = []
            for i in range(self.audio.get_device_count()):
                dev_info = self.audio.get_device_info_by_index(i)
                if dev_info.get('maxInputChannels') > 0:
                    device_name = dev_info.get('name')
                    input_devices.append((i, device_name))
                    logger.info(f"🎤 Input Device {i}: {device_name}")
            
            if not input_devices:
                logger.error("❌ No input devices found")
                return False
            
            # Try to open audio stream
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=AUDIO_FRAMES_PER_BUFFER,
                input_device_index=None  # Use default device
            )
            
            # Test recording a small sample
            logger.info("🧪 Testing microphone access...")
            test_data = self.stream.read(AUDIO_FRAMES_PER_BUFFER, exception_on_overflow=False)
            
            if len(test_data) > 0:
                logger.info("✅ Microphone access confirmed")
                logger.info("✅ Audio system initialized")
                return True
            else:
                logger.error("❌ No audio data from microphone")
                return False
                
        except OSError as e:
            if "Invalid device" in str(e) or "Input overflowed" in str(e):
                logger.error("❌ Microphone permission denied or device unavailable")
                logger.error("💡 Check System Preferences > Security & Privacy > Microphone")
            else:
                logger.error(f"❌ Audio system error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to initialize audio: {e}")
            return False
    
    def detect_voice_activity(self, audio_data: bytes, threshold: float = 0.005) -> bool:
        """Improved voice activity detection with multiple checks"""
        try:
            # Convert to numpy array
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            audio_np = audio_np / 32768.0
            
            # Calculate RMS energy (lowered threshold)
            rms = np.sqrt(np.mean(audio_np ** 2))
            
            # Calculate zero crossing rate (speech has higher ZCR than noise)
            zero_crossings = np.sum(np.diff(np.sign(audio_np)) != 0)
            zcr = zero_crossings / len(audio_np)
            
            # Check both energy and zero crossing rate
            has_energy = rms > threshold
            has_speech_characteristics = zcr > 0.01  # Speech typically has ZCR > 0.01
            
            # Log activity detection for debugging
            if has_energy:
                logger.debug(f"🔊 Voice activity - RMS: {rms:.4f}, ZCR: {zcr:.4f}")
            
            return has_energy and has_speech_characteristics
        except Exception as e:
            logger.error(f"Voice activity detection error: {e}")
            return True  # Default to processing if detection fails
    
    def record_audio_chunk(self) -> Optional[bytes]:
        """Record a chunk of audio with voice activity detection"""
        try:
            frames = []
            frames_needed = int(self.sample_rate * self.chunk_duration / AUDIO_FRAMES_PER_BUFFER)
            
            for _ in range(frames_needed):
                data = self.stream.read(AUDIO_FRAMES_PER_BUFFER, exception_on_overflow=False)
                frames.append(data)
            
            audio_data = b''.join(frames)
            
            # Check if there's actual voice activity
            if not self.detect_voice_activity(audio_data):
                return None  # Skip silent audio
            
            return audio_data
        except Exception as e:
            logger.error(f"❌ Error recording audio: {e}")
            return None
    
    def preprocess_audio(self, audio_np: np.ndarray) -> np.ndarray:
        """Preprocess audio to improve recognition accuracy"""
        try:
            # Apply high-pass filter to remove low-frequency noise
            from scipy.signal import butter, filtfilt
            
            # Ensure consistent dtype (float64) for scipy operations
            audio_np = audio_np.astype(np.float64)
            
            nyquist = self.sample_rate // 2
            low_cutoff = 300 / nyquist  # Remove frequencies below 300Hz
            b, a = butter(2, low_cutoff, btype='high')
            audio_np = filtfilt(b, a, audio_np)
            
            # Convert back to float32 for Whisper
            audio_np = audio_np.astype(np.float32)
            
            # Normalize volume
            max_val = np.max(np.abs(audio_np))
            if max_val > 0:
                audio_np = audio_np / max_val * 0.95
            
            return audio_np
        except ImportError:
            # If scipy not available, just normalize
            max_val = np.max(np.abs(audio_np))
            if max_val > 0:
                audio_np = audio_np / max_val * 0.95
            return audio_np
        except Exception as e:
            logger.warning(f"Audio preprocessing failed: {e}")
            return audio_np

    def transcribe_audio(self, audio_data: bytes) -> Optional[str]:
        """Transcribe audio using Whisper with improved preprocessing"""
        try:
            # Convert bytes to numpy array
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            
            # Normalize to [-1, 1] range
            audio_np = audio_np / 32768.0
            
            # Whisper expects 16kHz audio
            if len(audio_np) == 0:
                logger.warning("⚠️ Empty audio data")
                return None
            
            # Preprocess audio for better recognition
            audio_np = self.preprocess_audio(audio_np)
            
            # Transcribe with Whisper with more aggressive settings
            result = self.model.transcribe(
                audio_np, 
                language="en",
                word_timestamps=False,
                no_speech_threshold=0.3,  # More lenient no-speech detection
                logprob_threshold=-1.0,   # More lenient probability threshold
                compression_ratio_threshold=2.4,
                temperature=0.0  # Deterministic output
            )
            text = result["text"].strip()
            
            if text:
                logger.info(f"🎤 Transcribed: '{text}' (confidence: {result.get('segments', [{}])[0].get('avg_logprob', 'N/A') if result.get('segments') else 'N/A'})")
                return text.lower()
            else:
                logger.info("🔇 No speech detected in audio")
                return None
            
        except Exception as e:
            logger.error(f"❌ Transcription error: {e}")
            return None
    
    def is_valid_command(self, text: str) -> bool:
        """Check if transcribed text looks like a valid space command"""
        if not text:
            return False
        
        # Common space/navigation keywords
        space_keywords = [
            'mars', 'jupiter', 'saturn', 'venus', 'earth', 'moon', 'sun', 'mercury',
            'neptune', 'uranus', 'pluto', 'go', 'take', 'land', 'fly', 'travel',
            'navigate', 'screenshot', 'photo', 'camera', 'free', 'stop', 'back',
            'space', 'track', 'follow', 'explore', 'tour', 'visit', 'show'
        ]
        
        # Check if text contains any space-related keywords
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in space_keywords)
    
    def process_command(self, text: str) -> bool:
        """
        Process transcribed text as direct commands
        
        Args:
            text: Transcribed speech text
            
        Returns:
            bool: True if command was processed, False otherwise
        """
        if not text:
            return False
        
        # Clean up the text
        text = text.strip()
        
        # Check minimum length to avoid processing random sounds
        words = text.split()
        if len(words) < self.min_speech_length:
            logger.info(f"🔇 Speech too short: '{text}' ({len(words)} words)")
            return False
        
        # Filter out non-space-related transcriptions
        if not self.is_valid_command(text):
            logger.info(f"🚫 Not a space command: '{text}' - ignoring")
            return False
        
        logger.info(f"🎤 Valid Command: '{text}'")
        
        # Execute command callback directly
        if self.command_callback:
            try:
                self.command_callback(text)
                return True
            except Exception as e:
                logger.error(f"❌ Command execution error: {e}")
        else:
            logger.warning("⚠️ No command callback registered")
        
        return False
    
    def listen_continuously(self):
        """Main listening loop with voice activity detection and indicators"""
        logger.info("🎧 Starting continuous listening for direct commands")
        logger.info("💡 Say commands directly to control Gaia Sky")
        logger.info("💡 Example: 'Take me to Mars'")
        
        print("🟢 READY TO LISTEN - Speak clearly and say your command!")
        last_ready_time = time.time()
        
        while self.is_listening:
            try:
                # Show ready indicator every 10 seconds
                current_time = time.time()
                if current_time - last_ready_time > 10:
                    print("🟢 READY - Say your command now...")
                    last_ready_time = current_time
                
                # Record audio chunk (with voice activity detection)
                audio_data = self.record_audio_chunk()
                if not audio_data:
                    # No voice activity detected, continue listening
                    time.sleep(0.1)
                    continue
                
                # Voice detected! Show processing indicator
                print("🔴 PROCESSING SPEECH...")
                
                # Transcribe audio
                text = self.transcribe_audio(audio_data)
                if text:
                    print(f"🎤 Heard: '{text}'")
                    self.process_command(text)
                    print("🟢 READY - Say your next command...")
                    last_ready_time = time.time()
                else:
                    print("🟡 No clear speech detected, try again...")
                    print("🟢 READY - Say your command now...")
                    last_ready_time = time.time()
                
                # Small delay to prevent excessive processing
                time.sleep(0.2)
                
            except KeyboardInterrupt:
                logger.info("🛑 Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"❌ Error in listening loop: {e}")
                print("🟡 Audio error, retrying...")
                time.sleep(1)  # Wait before retrying
    
    def start_listening(self, command_callback: Callable[[str], None]) -> bool:
        """
        Start listening for speech commands
        
        Args:
            command_callback: Function to call when command is detected
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.is_listening:
            logger.warning("⚠️ Already listening")
            return False
        
        # Store callback
        self.command_callback = command_callback
        
        # Load model and setup audio
        if not self.model and not self.load_model():
            return False
        
        if not self.audio and not self.setup_audio():
            return False
        
        # Start listening in background thread
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self.listen_continuously, daemon=True)
        self.listen_thread.start()
        
        logger.info("🎤 Direct command recognition started!")
        return True
    
    def stop_listening(self):
        """Stop listening for speech commands"""
        if not self.is_listening:
            return
        
        logger.info("🛑 Stopping speech recognition...")
        self.is_listening = False
        
        # Wait for thread to finish
        if hasattr(self, 'listen_thread'):
            self.listen_thread.join(timeout=2.0)
        
        # Cleanup
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.audio:
            self.audio.terminate()
        
        logger.info("✅ Speech recognition stopped")
    
    def __del__(self):
        """Cleanup resources"""
        self.stop_listening()


# Demo function for testing
def demo_speech_recognition():
    """Demo function to test speech recognition"""
    
    def handle_command(command: str):
        print(f"🚀 COMMAND RECEIVED: {command}")
        print(f"📝 Would execute: {command}")
    
    recognizer = AstroSpeechRecognizer()
    
    try:
        print("🎤 Starting Astro Speech Recognition Demo")
        print("🎯 Using Whisper Base model with direct commands")
        print("💡 Say commands directly (no wake word needed)")
        print("💡 Example: 'Take me to Mars'")
        print("💡 Press Ctrl+C to stop")
        
        if recognizer.start_listening(handle_command):
            # Keep running until interrupted
            while True:
                time.sleep(1)
        else:
            print("❌ Failed to start speech recognition")
    
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    finally:
        recognizer.stop_listening()


if __name__ == "__main__":
    demo_speech_recognition()