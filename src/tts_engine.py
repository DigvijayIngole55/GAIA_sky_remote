#!/usr/bin/env python3
"""
🚀 COQUI TTS ENGINE
Professional neural text-to-speech for space navigation
Provides natural, contextual voice responses for hands-free operation
"""

import threading
import logging
import time
import os
from typing import Optional, Dict
from pathlib import Path

try:
    from .utils.config import (
        TTS_ENABLED, TTS_ENGINE, TTS_RATE, TTS_VOICE_INDEX, TTS_URGENT_RATE
    )
    from .audio_coordinator import get_audio_state_manager
except ImportError:
    from utils.config import (
        TTS_ENABLED, TTS_ENGINE, TTS_RATE, TTS_VOICE_INDEX, TTS_URGENT_RATE
    )
    from audio_coordinator import get_audio_state_manager

logger = logging.getLogger(__name__)

class CoquiTTSEngine:
    """
    Professional TTS engine using Coqui neural models
    Designed for natural space navigation voice responses
    """
    
    def __init__(self, model_name: str = "tts_models/en/ljspeech/tacotron2-DDC"):
        self.model_name = model_name
        self.tts = None
        self.enabled = TTS_ENABLED
        self._lock = threading.Lock()
        self._model_loaded = False
        
        # Audio coordination
        self.audio_manager = get_audio_state_manager()
        
        # Enhanced response templates for space navigation
        self.navigation_responses = {
            # Basic system status
            "connecting": "Connecting to Gaia Sky navigation system",
            "connected": "Navigation system connected and ready",
            "ready": "Navigation system ready for voice commands",
            "listening": "Listening for voice commands",
            "processing": "Processing your navigation request",
            "executing": "Executing navigation command",
            "complete": "Navigation command completed successfully",
            "done": "Operation completed",
            "failed": "Unable to execute command, please try again",
            "error": "System error encountered",
            "unclear": "Command unclear, please speak again",
            "got_it": "Command received and understood",
            "navigation_failed": "Navigation failed, please try again",
            "connection_failed": "Unable to connect to Gaia Sky",
            
            # Space navigation specific
            "mars_navigation": "Plotting course to Mars, estimated arrival time 6 months",
            "jupiter_approach": "Approaching Jupiter's gravitational field, adjusting trajectory",
            "screenshot_taken": "Screenshot captured of current view, saved to navigation database",
            "location_not_found": "Unable to locate that celestial body, please try again",
            "course_set": "Course successfully set, engaging autopilot systems",
            "orbit_established": "Orbital trajectory established around target body",
            "landing_sequence": "Initiating landing sequence, stand by for surface contact",
            "docking_complete": "Docking maneuver completed successfully",
            "system_online": "All navigation systems are online and operational"
        }
        
        if self.enabled:
            # Load model in background to avoid blocking
            threading.Thread(target=self._initialize_engine, daemon=True).start()
    
    def _initialize_engine(self):
        """Initialize the Coqui TTS engine"""
        try:
            logger.info("🔄 Loading Coqui TTS neural model...")
            start_time = time.time()
            
            from TTS.api import TTS
            self.tts = TTS(self.model_name)
            
            load_time = time.time() - start_time
            self._model_loaded = True
            logger.info(f"✅ Coqui TTS model loaded in {load_time:.2f}s: {self.model_name}")
            
        except ImportError as e:
            logger.warning(f"⚠️ Coqui TTS not installed: {e}")
            logger.warning("💡 Install with: pip install TTS")
            self.enabled = False
        except Exception as e:
            logger.error(f"❌ Coqui TTS initialization failed: {e}")
            self.enabled = False
    
    def speak_indicator(self, indicator_type: str, background: bool = True):
        """
        Speak a navigation status indicator with enhanced messages
        
        Args:
            indicator_type: Type of indicator (connecting, ready, processing, etc.)
            background: Whether to speak in background thread
        """
        if not self.enabled:
            return
            
        message = self.navigation_responses.get(indicator_type, indicator_type)
        self.speak_text(message, background=background)
    
    def speak_navigation_status(self, status_type: str, context: str = "", background: bool = True):
        """
        Speak context-aware navigation status
        
        Args:
            status_type: Type of status (course_set, screenshot_taken, etc.)
            context: Additional context to include
            background: Whether to speak in background thread
        """
        if not self.enabled:
            return
            
        base_message = self.navigation_responses.get(status_type, status_type)
        
        # Add context if provided
        if context:
            message = f"{base_message}. {context}"
        else:
            message = base_message
            
        self.speak_text(message, background=background)
    
    def speak_text(self, text: str, background: bool = True):
        """
        Speak custom text using neural TTS
        
        Args:
            text: Text to speak
            background: Whether to speak in background thread
        """
        if not self.enabled:
            return
            
        if background:
            threading.Thread(target=self._speak_text, args=(text,), daemon=True).start()
        else:
            self._speak_text(text)
    
    def speak_text_sync(self, text: str):
        """
        Speak custom text synchronously (blocking)
        
        Args:
            text: Text to speak
        """
        if not self.enabled:
            return
        
        # Always call synchronously without audio coordination
        self._speak_text_direct(text)
    
    def speak_indicator_sync(self, indicator_type: str):
        """
        Speak indicator synchronously (blocking)
        
        Args:
            indicator_type: Type of indicator to speak
        """
        if not self.enabled:
            return
            
        message = self.navigation_responses.get(indicator_type, indicator_type)
        self.speak_text_sync(message)
    
    def _speak_text(self, text: str):
        """Internal method to handle actual speech synthesis with audio coordination"""
        if not self.enabled:
            return
            
        # Wait for model to load if necessary
        if not self._model_loaded:
            logger.info("⏳ Waiting for TTS model to load...")
            for _ in range(50):  # Wait up to 5 seconds
                if self._model_loaded:
                    break
                time.sleep(0.1)
            
            if not self._model_loaded:
                logger.warning("⚠️ TTS model not ready, skipping speech")
                return
        
        # Request permission to speak (this will pause speech recognition)
        if not self.audio_manager.request_tts_permission(timeout=3.0):
            logger.warning("⚠️ Could not get TTS permission, skipping speech")
            return
        
        try:
            # Signal TTS started
            self.audio_manager.signal_tts_started()
            
            with self._lock:
                # Generate temporary audio file
                temp_file = "/tmp/tts_output.wav"
                
                logger.debug(f"🎤 Synthesizing: '{text[:50]}{'...' if len(text) > 50 else ''}'")
                start_time = time.time()
                
                self.tts.tts_to_file(text=text, file_path=temp_file)
                
                synthesis_time = time.time() - start_time
                logger.debug(f"🔊 Synthesis completed in {synthesis_time:.2f}s")
                
                # Play the audio file and wait for completion
                if os.path.exists(temp_file):
                    import subprocess
                    # Use subprocess.run instead of os.system to wait for completion
                    try:
                        subprocess.run(["afplay", temp_file], check=True, timeout=10)
                        logger.debug("🔊 Audio playback completed")
                    except subprocess.TimeoutExpired:
                        logger.warning("⚠️ Audio playback timeout")
                    except subprocess.CalledProcessError as e:
                        logger.error(f"❌ Audio playback failed: {e}")
                    
                    # Clean up
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                
        except Exception as e:
            logger.error(f"❌ TTS speech synthesis failed: {e}")
        finally:
            # Always signal TTS finished to resume speech recognition
            self.audio_manager.signal_tts_finished()
    
    def _speak_text_direct(self, text: str):
        """
        Internal method for direct speech synthesis WITH audio coordination
        Used for synchronous sequential voice control
        """
        if not self.enabled:
            return
            
        # Wait for model to load if necessary
        if not self._model_loaded:
            logger.info("⏳ Waiting for TTS model to load...")
            for _ in range(50):  # Wait up to 5 seconds
                if self._model_loaded:
                    break
                time.sleep(0.1)
            
            if not self._model_loaded:
                logger.warning("⚠️ TTS model not ready, skipping speech")
                return
        
        try:
            # Signal TTS started - coordinate with speech recognition
            self.audio_manager.signal_tts_started()
            
            with self._lock:
                # Generate temporary audio file
                temp_file = "/tmp/tts_output.wav"
                
                logger.debug(f"🎤 Synthesizing: '{text[:50]}{'...' if len(text) > 50 else ''}'")
                start_time = time.time()
                
                self.tts.tts_to_file(text=text, file_path=temp_file)
                
                synthesis_time = time.time() - start_time
                logger.debug(f"🔊 Synthesis completed in {synthesis_time:.2f}s")
                
                # Play the audio file and wait for completion
                if os.path.exists(temp_file):
                    import subprocess
                    # Use subprocess.run instead of os.system to wait for completion
                    try:
                        subprocess.run(["afplay", temp_file], check=True, timeout=10)
                        logger.debug("🔊 Audio playback completed")
                    except subprocess.TimeoutExpired:
                        logger.warning("⚠️ Audio playback timeout")
                    except subprocess.CalledProcessError as e:
                        logger.error(f"❌ Audio playback failed: {e}")
                    
                    # Clean up
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                
        except Exception as e:
            logger.error(f"❌ TTS speech synthesis failed: {e}")
        finally:
            # Always signal TTS finished to resume speech recognition
            self.audio_manager.signal_tts_finished()
    
    def stop(self):
        """Stop current speech and cleanup"""
        # Coqui TTS doesn't have a direct stop method
        # Kill any running afplay processes
        try:
            os.system("pkill afplay")
        except Exception as e:
            logger.warning(f"⚠️ TTS stop failed: {e}")
    
    def is_enabled(self) -> bool:
        """Check if TTS is enabled and working"""
        return self.enabled and self._model_loaded
    
    def is_ready(self) -> bool:
        """Check if TTS model is loaded and ready"""
        return self._model_loaded
    
    def get_available_responses(self) -> Dict[str, str]:
        """Get all available navigation responses"""
        return self.navigation_responses.copy()

# Convenience functions for easy import
def create_tts_engine() -> CoquiTTSEngine:
    """Create and return a Coqui TTS engine instance"""
    return CoquiTTSEngine()

def speak_indicator(indicator_type: str, tts_engine: Optional[CoquiTTSEngine] = None):
    """Convenience function to speak an indicator"""
    if tts_engine and tts_engine.is_enabled():
        tts_engine.speak_indicator(indicator_type)

def speak_navigation_status(status_type: str, context: str = "", tts_engine: Optional[CoquiTTSEngine] = None):
    """Convenience function to speak navigation status"""
    if tts_engine and tts_engine.is_enabled():
        tts_engine.speak_navigation_status(status_type, context)

# Legacy compatibility - maintaining old interface
UniversalTTSEngine = CoquiTTSEngine  # Alias for backward compatibility

def speak_cue(cue_type: str, tts_engine: Optional[CoquiTTSEngine] = None):
    """Legacy function - maps old cues to new indicators"""
    if tts_engine and tts_engine.is_enabled():
        tts_engine.speak_indicator(cue_type)