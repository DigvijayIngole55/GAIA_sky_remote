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
    from .tts_engine import CoquiTTSEngine
    from .audio_coordinator import get_audio_state_manager
except ImportError:
    # Fallback for direct execution
    from utils.config import (
        WHISPER_MODEL_SIZE, SAMPLE_RATE, CHUNK_DURATION, 
        MIN_SPEECH_LENGTH, AUDIO_CHANNELS, AUDIO_FRAMES_PER_BUFFER
    )
    from tts_engine import CoquiTTSEngine
    from audio_coordinator import get_audio_state_manager

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
        self.tts_engine = None  # TTS for voice cues
        
        # Audio coordination
        self.audio_manager = get_audio_state_manager()
        
        logger.info("🎤 Astro Speech Recognizer initialized for direct commands")
    
    def set_tts_engine(self, tts_engine):
        """Set TTS engine for voice cues"""
        self.tts_engine = tts_engine
    
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
    
    
    def record_audio_chunk(self) -> Optional[bytes]:
        """Record a chunk of audio - let Whisper handle silence detection"""
        try:
            frames = []
            frames_needed = int(self.sample_rate * self.chunk_duration / AUDIO_FRAMES_PER_BUFFER)
            
            for _ in range(frames_needed):
                data = self.stream.read(AUDIO_FRAMES_PER_BUFFER, exception_on_overflow=False)
                frames.append(data)
            
            audio_data = b''.join(frames)
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
            
            # Transcribe with Whisper - original working settings
            result = self.model.transcribe(
                audio_np, 
                language="en",
                word_timestamps=False,
                no_speech_threshold=0.3,  # Original working value
                logprob_threshold=-1.0,   
                compression_ratio_threshold=2.4,
                temperature=0.0
            )
            text = result["text"].strip()
            
            if text:
                # Check for Whisper hallucinations (repetitive phrases)
                if self.is_hallucination(text):
                    logger.info(f"🚫 Detected hallucination: '{text[:50]}...' - ignoring")
                    return None
                
                logger.info(f"🎤 Transcribed: '{text}' (confidence: {result.get('segments', [{}])[0].get('avg_logprob', 'N/A') if result.get('segments') else 'N/A'})")
                return text.lower()
            else:
                logger.info("🔇 No speech detected in audio")
                return None
            
        except Exception as e:
            logger.error(f"❌ Transcription error: {e}")
            return None
    
    def is_hallucination(self, text: str) -> bool:
        """Detect if text is a Whisper hallucination (repetitive phrases)"""
        if not text or len(text) < 20:
            return False
        
        # Check for repetitive patterns
        words = text.split()
        if len(words) < 4:
            return False
        
        # Check if more than 50% of words are repetitive
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        max_repeats = max(word_counts.values())
        repetitive_ratio = max_repeats / len(words)
        
        # If more than 40% repetition, likely hallucination
        if repetitive_ratio > 0.4:
            return True
        
        # Check for specific hallucination patterns
        hallucination_patterns = [
            "and then the",
            "the sound of the sound",
            "and the next one",
            "and then and then",
            "the the the"
        ]
        
        text_lower = text.lower()
        for pattern in hallucination_patterns:
            if pattern in text_lower:
                return True
        
        return False
    
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
        Process transcribed text as direct commands (original working version)
        
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
        """Main listening loop with audio coordination to prevent feedback"""
        logger.info("🎧 Starting continuous listening for direct commands")
        logger.info("💡 Say commands directly to control Gaia Sky")
        logger.info("💡 Example: 'Take me to Mars'")
        
        print("🟢 READY TO LISTEN - Speak clearly and say your command!")
        last_ready_time = time.time()
        
        while self.is_listening:
            try:
                # Check if we're allowed to listen (not during TTS playback)
                if not self.audio_manager.is_listening_allowed():
                    # TTS is speaking, pause listening
                    if not hasattr(self, '_paused_logged'):
                        logger.debug("🔇 Pausing speech recognition during TTS")
                        self.audio_manager.signal_speech_paused()
                        self._paused_logged = True
                    
                    # Wait for permission to resume listening with adequate timeout
                    self.audio_manager.request_listening_permission(timeout=2.0)
                    # Don't log errors - just continue
                    time.sleep(0.1)
                    continue
                
                # We have permission to listen
                if hasattr(self, '_paused_logged'):
                    logger.debug("🎧 Speech recognition resumed")
                    delattr(self, '_paused_logged')
                
                # Show ready indicator every 10 seconds
                current_time = time.time()
                if current_time - last_ready_time > 10:
                    print("🟢 READY - Say your command now...")
                    last_ready_time = current_time
                
                # Record audio chunk - only if listening is allowed
                if not self.audio_manager.is_listening_allowed():
                    time.sleep(0.1)
                    continue
                
                audio_data = self.record_audio_chunk()
                if not audio_data:
                    # Error recording, try again
                    time.sleep(0.1)
                    continue
                
                # Voice detected! Show processing indicator
                print("🔴 PROCESSING SPEECH...")
                
                # Signal processing started
                self.audio_manager.signal_processing_started()
                
                try:
                    # Transcribe audio
                    text = self.transcribe_audio(audio_data)
                    if text:
                        print(f"🎤 Heard: '{text}'")
                        # Process command and only give confirmation if successful
                        command_processed = self.process_command(text)
                        if command_processed:
                            # NOTE: TTS feedback is now handled within the command execution
                            # No additional "got_it" confirmation needed to avoid duplicate responses
                            print("🟢 READY - Say your next command...")
                        else:
                            print("🟢 READY - Say your command now...")
                        last_ready_time = time.time()
                    else:
                        print("🟡 No clear speech detected, try again...")
                        print("🟢 READY - Say your command now...")
                        last_ready_time = time.time()
                finally:
                    # Always signal processing finished
                    self.audio_manager.signal_processing_finished()
                
                # Small delay to prevent excessive processing
                time.sleep(0.2)
                
            except KeyboardInterrupt:
                logger.info("🛑 Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"❌ Error in listening loop: {e}")
                print("🟡 Audio error, retrying...")
                # Signal processing finished on error
                self.audio_manager.signal_processing_finished()
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
    
    def listen_once(self, timeout: float = 30.0) -> Optional[str]:
        """
        Listen for a single command (blocking, synchronous)
        
        Args:
            timeout: Maximum time to wait for valid command
            
        Returns:
            Command text or None if timeout/error
        """
        if not self.model and not self.load_model():
            logger.error("❌ Cannot listen - Whisper model not loaded")
            return None
        
        if not self.audio and not self.setup_audio():
            logger.error("❌ Cannot listen - Audio system not ready")
            return None
        
        logger.debug(f"🎧 Listening for single command (timeout: {timeout}s)")
        
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            try:
                # Record audio chunk
                audio_data = self.record_audio_chunk()
                if not audio_data:
                    time.sleep(0.1)
                    continue
                
                # Transcribe audio
                text = self.transcribe_audio(audio_data)
                if text:
                    # Check if it's a valid command
                    if self.is_valid_command(text):
                        logger.info(f"🎤 Valid command captured: '{text}'")
                        return text
                    else:
                        logger.debug(f"🚫 Invalid command ignored: '{text}'")
                        # Continue listening for valid command
                        continue
                
                # Small delay before next attempt
                time.sleep(0.2)
                
            except Exception as e:
                logger.error(f"❌ Listen once error: {e}")
                return None
        
        logger.warning(f"⏰ Listen once timeout after {timeout}s")
        return None
    
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
    
    recognizer = UniversalSpeechRecognizer()
    
    try:
        print("🎤 Starting Astro Speech Recognition Demo")
        print("🎯 Using Whisper Base model with ASTRO wake word")
        print("💡 Say 'ASTRO' followed by your command")
        print("💡 Example: 'ASTRO take me to Mars'")
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