#!/usr/bin/env python3
"""
🎤 SEQUENTIAL VOICE CONTROLLER
Sequential state machine for voice control - no async overlaps or feedback loops
"""

import time
import logging
from enum import Enum
from typing import Optional, Callable

# Configure logging
logger = logging.getLogger(__name__)

class VoiceState(Enum):
    """Sequential voice control states"""
    IDLE = "idle"
    SPEAKING = "speaking"
    LISTENING = "listening" 
    PROCESSING = "processing"
    EXECUTING = "executing"
    FEEDBACK = "feedback"

class SequentialVoiceController:
    """
    Sequential voice controller that ensures proper state transitions
    One operation at a time - no concurrent audio operations
    """
    
    def __init__(self, tts_engine, speech_recognizer, command_executor):
        """
        Initialize sequential voice controller
        
        Args:
            tts_engine: TTS engine for speech output
            speech_recognizer: Speech recognition engine
            command_executor: Function to execute commands
        """
        self.tts_engine = tts_engine
        self.speech_recognizer = speech_recognizer
        self.command_executor = command_executor
        
        self.current_state = VoiceState.IDLE
        self.is_running = False
        
        logger.info("🎤 Sequential Voice Controller initialized")
    
    def _change_state(self, new_state: VoiceState):
        """Change state with logging"""
        old_state = self.current_state
        self.current_state = new_state
        logger.debug(f"State: {old_state.value} → {new_state.value}")
    
    def speak_and_wait(self, text: str, indicator_type: Optional[str] = None):
        """
        Speak text and wait for completion (blocking)
        
        Args:
            text: Text to speak or indicator type
            indicator_type: If provided, use speak_indicator instead
        """
        self._change_state(VoiceState.SPEAKING)
        
        logger.debug(f"🔊 Speaking: {text}")
        
        if indicator_type:
            # Use TTS indicator (synchronous)
            self.tts_engine.speak_indicator_sync(indicator_type)
        else:
            # Use custom text (synchronous)
            self.tts_engine.speak_text_sync(text)
        
        logger.debug("🔊 Speech completed")
        self._change_state(VoiceState.IDLE)
    
    def listen_for_command(self, timeout: float = 30.0) -> Optional[str]:
        """
        Listen for a single command (blocking)
        
        Args:
            timeout: Maximum time to wait for command
            
        Returns:
            Command text or None if timeout/error
        """
        self._change_state(VoiceState.LISTENING)
        
        logger.debug("🎧 Listening for command...")
        print("🟢 READY - Say your command now...")
        
        try:
            # Use synchronous single-command listening
            command = self.speech_recognizer.listen_once(timeout=timeout)
            
            if command:
                logger.info(f"🎤 Command received: '{command}'")
                print(f"🎤 Heard: '{command}'")
                self._change_state(VoiceState.IDLE)
                return command
            else:
                logger.debug("🔇 No command received")
                print("🟡 No command heard, try again...")
                self._change_state(VoiceState.IDLE)
                return None
                
        except Exception as e:
            logger.error(f"❌ Listening error: {e}")
            print("🟡 Audio error, retrying...")
            self._change_state(VoiceState.IDLE)
            return None
    
    def process_and_execute_command(self, command: str) -> str:
        """
        Process and execute command (blocking)
        
        Args:
            command: Command text to execute
            
        Returns:
            Execution result
        """
        self._change_state(VoiceState.PROCESSING)
        
        logger.debug(f"⚙️ Processing command: {command}")
        print("🔴 PROCESSING COMMAND...")
        
        try:
            # Execute command synchronously
            self._change_state(VoiceState.EXECUTING)
            print("⚡ EXECUTING ON GAIA SKY...")
            
            result = self.command_executor(command)
            
            logger.info(f"✅ Command result: {result}")
            self._change_state(VoiceState.IDLE)
            return result
            
        except Exception as e:
            logger.error(f"❌ Command execution error: {e}")
            self._change_state(VoiceState.IDLE)
            return f"❌ Command failed: {str(e)}"
    
    def give_feedback(self, result: str):
        """
        Give voice feedback based on result (blocking)
        
        Args:
            result: Command execution result
        """
        self._change_state(VoiceState.FEEDBACK)
        
        logger.debug(f"📢 Giving feedback for result: {result[:50]}...")
        
        # Determine appropriate feedback
        if result.startswith("❌"):
            # Error result
            error_msg = result.replace("❌", "").strip()
            if "connection" in error_msg.lower():
                self.speak_and_wait("", indicator_type="connection_failed")
            elif "navigation" in error_msg.lower() and "failed" in error_msg.lower():
                self.speak_and_wait("", indicator_type="navigation_failed")
            else:
                self.speak_and_wait("", indicator_type="error")
                
        elif result.startswith("✈️") or "successfully" in result.lower():
            # Success result
            self.speak_and_wait("", indicator_type="complete")
            
        elif result.startswith("📸"):
            # Screenshot result
            self.speak_and_wait("", indicator_type="screenshot_taken")
            
        else:
            # Generic completion
            self.speak_and_wait("", indicator_type="done")
        
        self._change_state(VoiceState.IDLE)
    
    def run_voice_control_loop(self):
        """
        Main sequential voice control loop
        Each operation blocks until completion
        """
        logger.info("🚀 Starting sequential voice control loop")
        
        self.is_running = True
        
        # Initial greeting
        self.speak_and_wait("", indicator_type="ready")
        
        while self.is_running:
            try:
                # Step 1: Listen for command (blocking)
                command = self.listen_for_command(timeout=30.0)
                
                if not command:
                    # No command received, continue listening
                    continue
                
                # Step 2: Process and execute command (blocking)
                result = self.process_and_execute_command(command)
                
                # Step 3: Give voice feedback (blocking)
                self.give_feedback(result)
                
                # Small pause before next iteration
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                logger.info("🛑 Voice control interrupted by user")
                break
            except Exception as e:
                logger.error(f"❌ Voice control loop error: {e}")
                self.speak_and_wait("", indicator_type="error")
                time.sleep(1)
        
        logger.info("🔚 Sequential voice control loop ended")
    
    def stop(self):
        """Stop the voice control loop"""
        logger.info("🛑 Stopping voice control...")
        self.is_running = False
        self._change_state(VoiceState.IDLE)
    
    def get_status(self) -> dict:
        """Get current status"""
        return {
            "current_state": self.current_state.value,
            "is_running": self.is_running
        }

def create_sequential_voice_controller(tts_engine, speech_recognizer, command_executor):
    """
    Factory function to create sequential voice controller
    
    Args:
        tts_engine: TTS engine instance
        speech_recognizer: Speech recognizer instance  
        command_executor: Command execution function
        
    Returns:
        SequentialVoiceController instance
    """
    return SequentialVoiceController(tts_engine, speech_recognizer, command_executor)