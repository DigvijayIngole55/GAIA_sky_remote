#!/usr/bin/env python3
"""
🎵 AUDIO COORDINATOR
Manages coordination between TTS and speech recognition to prevent feedback loops
"""

import threading
import logging
import time
from enum import Enum
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)

class AudioState(Enum):
    """Audio system states"""
    LISTENING = "listening"      # Microphone active, TTS silent
    SPEAKING = "speaking"        # TTS active, microphone muted
    PROCESSING = "processing"    # Both paused during command processing
    IDLE = "idle"               # Neither active

class AudioStateManager:
    """
    Singleton coordinator for TTS and speech recognition audio systems
    Prevents feedback loops by ensuring only one audio system is active at a time
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize audio state manager"""
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.current_state = AudioState.IDLE
        self.state_lock = threading.RLock()
        
        # Events for coordination
        self.tts_finished_event = threading.Event()
        self.speech_paused_event = threading.Event()
        self.processing_complete_event = threading.Event()
        
        # State change callbacks
        self.state_change_callbacks = []
        
        logger.info("🎵 AudioStateManager initialized")
    
    def register_state_callback(self, callback):
        """Register callback for state changes"""
        self.state_change_callbacks.append(callback)
    
    def _notify_state_change(self, old_state: AudioState, new_state: AudioState):
        """Notify all registered callbacks of state change"""
        for callback in self.state_change_callbacks:
            try:
                callback(old_state, new_state)
            except Exception as e:
                logger.error(f"State change callback error: {e}")
    
    def get_current_state(self) -> AudioState:
        """Get current audio state"""
        with self.state_lock:
            return self.current_state
    
    def is_listening_allowed(self) -> bool:
        """Check if speech recognition should be active"""
        with self.state_lock:
            return self.current_state in [AudioState.LISTENING, AudioState.IDLE]
    
    def is_tts_allowed(self) -> bool:
        """Check if TTS should be active"""
        with self.state_lock:
            return self.current_state in [AudioState.SPEAKING, AudioState.IDLE]
    
    def request_tts_permission(self, timeout: float = 2.0) -> bool:
        """
        Request permission to start TTS (blocks until speech is paused)
        
        Args:
            timeout: Maximum time to wait for permission
            
        Returns:
            bool: True if permission granted, False if timeout
        """
        logger.debug("🎤 Requesting TTS permission...")
        
        with self.state_lock:
            # If already speaking, grant immediately
            if self.current_state == AudioState.SPEAKING:
                return True
            
            # If idle, transition directly to speaking
            if self.current_state == AudioState.IDLE:
                old_state = self.current_state
                self.current_state = AudioState.SPEAKING
                self._notify_state_change(old_state, self.current_state)
                logger.debug("🔊 TTS permission granted (idle->speaking)")
                return True
            
            # If listening, transition to speaking immediately (more aggressive)
            if self.current_state == AudioState.LISTENING:
                old_state = self.current_state
                self.current_state = AudioState.SPEAKING
                self._notify_state_change(old_state, self.current_state)
                
                # Signal that speech should pause and give a very short wait
                self.speech_paused_event.set()  # Pre-signal
                
                # Very short wait just to be safe
                import time
                time.sleep(0.1)
                
                logger.debug("🔊 TTS permission granted (listening interrupted)")
                return True
            
            # Processing state - during processing, allow TTS but with shorter timeout
            if self.current_state == AudioState.PROCESSING:
                # Force transition to speaking
                old_state = self.current_state
                self.current_state = AudioState.SPEAKING
                self._notify_state_change(old_state, self.current_state)
                logger.debug("🔊 TTS permission granted (processing interrupted)")
                return True
        
        return True  # Always grant permission to avoid blocking
    
    def request_listening_permission(self, timeout: float = 1.0) -> bool:
        """
        Request permission to start listening (blocks until TTS finishes)
        
        Args:
            timeout: Maximum time to wait for permission
            
        Returns:
            bool: True if permission granted, False if timeout
        """
        logger.debug("🎧 Requesting listening permission...")
        
        with self.state_lock:
            # If already listening, grant immediately
            if self.current_state == AudioState.LISTENING:
                return True
            
            # If idle, transition directly to listening
            if self.current_state == AudioState.IDLE:
                old_state = self.current_state
                self.current_state = AudioState.LISTENING
                self._notify_state_change(old_state, self.current_state)
                logger.debug("🎧 Listening permission granted (idle->listening)")
                return True
            
            # If speaking, wait for TTS to finish with shorter timeout
            if self.current_state == AudioState.SPEAKING:
                if self.tts_finished_event.wait(timeout):
                    old_state = self.current_state
                    self.current_state = AudioState.LISTENING
                    self._notify_state_change(old_state, self.current_state)
                    logger.debug("🎧 Listening permission granted (TTS finished)")
                    return True
                else:
                    # Don't wait too long - just force transition if needed
                    old_state = self.current_state
                    self.current_state = AudioState.LISTENING
                    self._notify_state_change(old_state, self.current_state)
                    logger.debug("🎧 Listening permission granted (forced after timeout)")
                    return True
            
            # Processing state - always allow listening after processing
            if self.current_state == AudioState.PROCESSING:
                old_state = self.current_state
                self.current_state = AudioState.LISTENING
                self._notify_state_change(old_state, self.current_state)
                logger.debug("🎧 Listening permission granted (processing->listening)")
                return True
        
        return True  # Always grant permission to avoid blocking
    
    def signal_tts_started(self):
        """Signal that TTS has started speaking"""
        with self.state_lock:
            if self.current_state != AudioState.SPEAKING:
                old_state = self.current_state
                self.current_state = AudioState.SPEAKING
                self._notify_state_change(old_state, self.current_state)
            
            # Clear the TTS finished event
            self.tts_finished_event.clear()
            logger.debug("🔊 TTS started signal")
    
    def signal_tts_finished(self):
        """Signal that TTS has finished speaking"""
        with self.state_lock:
            if self.current_state == AudioState.SPEAKING:
                old_state = self.current_state
                self.current_state = AudioState.IDLE
                self._notify_state_change(old_state, self.current_state)
            
            # Notify waiting listeners
            self.tts_finished_event.set()
            logger.debug("🔊 TTS finished signal")
    
    def signal_speech_paused(self):
        """Signal that speech recognition has paused"""
        # Notify waiting TTS requests
        self.speech_paused_event.set()
        logger.debug("🎧 Speech paused signal")
    
    def signal_speech_resumed(self):
        """Signal that speech recognition has resumed"""
        with self.state_lock:
            if self.current_state != AudioState.LISTENING:
                old_state = self.current_state
                self.current_state = AudioState.LISTENING
                self._notify_state_change(old_state, self.current_state)
        
        # Clear the speech paused event
        self.speech_paused_event.clear()
        logger.debug("🎧 Speech resumed signal")
    
    def signal_processing_started(self):
        """Signal that command processing has started"""
        with self.state_lock:
            old_state = self.current_state
            self.current_state = AudioState.PROCESSING
            self._notify_state_change(old_state, self.current_state)
        
        # Clear processing complete event
        self.processing_complete_event.clear()
        logger.debug("⚙️ Processing started signal")
    
    def signal_processing_finished(self):
        """Signal that command processing has finished"""
        with self.state_lock:
            old_state = self.current_state
            self.current_state = AudioState.IDLE
            self._notify_state_change(old_state, self.current_state)
        
        # Notify waiting systems
        self.processing_complete_event.set()
        logger.debug("⚙️ Processing finished signal")
    
    def force_idle(self):
        """Force audio system to idle state (emergency reset)"""
        with self.state_lock:
            old_state = self.current_state
            self.current_state = AudioState.IDLE
            self._notify_state_change(old_state, self.current_state)
        
        # Set all events to unblock any waiting threads
        self.tts_finished_event.set()
        self.speech_paused_event.set()
        self.processing_complete_event.set()
        
        logger.info("🔄 Audio system forced to idle state")
    
    def get_status_summary(self) -> dict:
        """Get current status summary for debugging"""
        with self.state_lock:
            return {
                "current_state": self.current_state.value,
                "listening_allowed": self.is_listening_allowed(),
                "tts_allowed": self.is_tts_allowed(),
                "tts_finished_event_set": self.tts_finished_event.is_set(),
                "speech_paused_event_set": self.speech_paused_event.is_set(),
                "processing_complete_event_set": self.processing_complete_event.is_set()
            }

# Global instance
audio_state_manager = AudioStateManager()

def get_audio_state_manager() -> AudioStateManager:
    """Get the global audio state manager instance"""
    return audio_state_manager