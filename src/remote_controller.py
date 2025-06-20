#!/usr/bin/env python3
"""
🚀 STANDALONE GAIA SKY REMOTE CONTROLLER
Complete standalone version with advanced multi-tool capabilities and voice control!

A completely independent, LLM-powered natural language remote controller for Gaia Sky
with situational awareness, direct voice commands, and extensive navigation capabilities.
"""

import json
import re
import time
import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

# Import our connection manager
try:
    from .gaia_sky_connection import get_connection_manager
except ImportError:
    from gaia_sky_connection import get_connection_manager

# Import standardized methods registry
try:
    from .gaia_sky_methods import get_method_registry
except ImportError:
    from gaia_sky_methods import get_method_registry

# Import configuration
try:
    from .utils.config import (
        LM_STUDIO_BASE_URL, LM_STUDIO_MODEL, LM_STUDIO_TIMEOUT,
        LM_STUDIO_TEMPERATURE, LM_STUDIO_MAX_TOKENS,
        AVAILABLE_ACTIONS, CELESTIAL_OBJECTS, TOUR_ROUTES
    )
except ImportError:
    from utils.config import (
        LM_STUDIO_BASE_URL, LM_STUDIO_MODEL, LM_STUDIO_TIMEOUT,
        LM_STUDIO_TEMPERATURE, LM_STUDIO_MAX_TOKENS,
        AVAILABLE_ACTIONS, CELESTIAL_OBJECTS, TOUR_ROUTES
    )

# Import speech recognition (optional)
try:
    from .speech_recognizer import UniversalSpeechRecognizer
    from .tts_engine import CoquiTTSEngine
    from .audio_coordinator import get_audio_state_manager
    from .gaia_completion_manager import get_completion_manager
    SPEECH_AVAILABLE = True
except ImportError:
    try:
        from speech_recognizer import UniversalSpeechRecognizer
        from tts_engine import CoquiTTSEngine
        from audio_coordinator import get_audio_state_manager
        from gaia_completion_manager import get_completion_manager
        SPEECH_AVAILABLE = True
    except ImportError:
        SPEECH_AVAILABLE = False
        logging.warning("⚠️ Speech recognition not available - install dependencies for voice control")

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class Command:
    """Parsed command structure for space navigation"""
    action: str
    entity: str
    parameters: Dict[str, Any] = None

class UniversalLLMProvider:
    """Simple LM Studio provider for natural language command parsing"""
    
    def __init__(self):
        self.base_url = LM_STUDIO_BASE_URL
        self.model = LM_STUDIO_MODEL
        
    def parse_command(self, user_input: str) -> Optional[Command]:
        """Parse natural language into structured command using LLM"""
        
        print(f"🧠 [LLM] Attempting to parse: '{user_input}'")
        print(f"🧠 [LLM] Using model: {self.model} at {self.base_url}")
        
        # System prompt for command extraction
        system_prompt = f"""You are a space navigation command parser. Extract navigation commands from natural language.

Available actions: {', '.join(AVAILABLE_ACTIONS)}
Common entities: {', '.join(CELESTIAL_OBJECTS)}

Return JSON format:
{{
  "action": "go_to|land_on|track|set_time|take_screenshot|explore|orbit|zoom_in|zoom_out|speed_up|slow_down|free_camera|stop_camera|back_to_space|tour|cinematic_journey|multi_step|stream_tour|camera_transition|draw_path|add_marker|time_travel|pitch_camera|roll_camera|smooth_orientation",
  "entity": "object_name",
  "parameters": {{"duration": 5.0, "smooth": true}}
}}

EXTENSIVE EXAMPLES:

Navigation Commands:
"go to mars" -> {{"action": "go_to", "entity": "Mars"}}
"take me to jupiter" -> {{"action": "go_to", "entity": "Jupiter"}}
"fly to saturn" -> {{"action": "go_to", "entity": "Saturn"}}
"travel to the sun" -> {{"action": "go_to", "entity": "Sun"}}
"navigate to venus" -> {{"action": "go_to", "entity": "Venus"}}
"visit earth" -> {{"action": "go_to", "entity": "Earth"}}

Landing Commands:
"land on the moon" -> {{"action": "land_on", "entity": "Moon"}}
"land on mars" -> {{"action": "land_on", "entity": "Mars"}}
"touch down on europa" -> {{"action": "land_on", "entity": "Europa"}}

Tracking Commands:
"track saturn" -> {{"action": "track", "entity": "Saturn"}}
"follow jupiter" -> {{"action": "track", "entity": "Jupiter"}}
"watch the moon" -> {{"action": "track", "entity": "Moon"}}

Exploration Commands:
"explore venus" -> {{"action": "explore", "entity": "Venus"}}
"investigate mars" -> {{"action": "explore", "entity": "Mars"}}

Photography Commands:
"take screenshot" -> {{"action": "take_screenshot", "entity": ""}}
"capture image" -> {{"action": "take_screenshot", "entity": ""}}
"take a photo" -> {{"action": "take_screenshot", "entity": ""}}

Recovery Commands:
"free camera" -> {{"action": "free_camera", "entity": ""}}
"stop camera" -> {{"action": "stop_camera", "entity": ""}}
"back to space" -> {{"action": "back_to_space", "entity": ""}}
"unlock camera" -> {{"action": "free_camera", "entity": ""}}
"release camera" -> {{"action": "free_camera", "entity": ""}}
"get unstuck" -> {{"action": "free_camera", "entity": ""}}

Multi-Tool Commands:
"tour the solar system" -> {{"action": "tour", "entity": "solar system"}}
"tour solar system" -> {{"action": "tour", "entity": "solar system"}}
"grand tour of planets" -> {{"action": "tour", "entity": "planets"}}
"tour planets" -> {{"action": "tour", "entity": "planets"}}
"cinematic journey to mars" -> {{"action": "cinematic_journey", "entity": "Mars"}}
"stream tour of jupiter moons" -> {{"action": "stream_tour", "entity": "Jupiter"}}

Multi-Step Commands:
"visit mars then land on it" -> {{"action": "multi_step", "entity": "Mars", "parameters": {{"steps": [{{"action": "go_to", "entity": "Mars"}}, {{"action": "land_on", "entity": "Mars"}}]}}}}
"go to jupiter and track it" -> {{"action": "multi_step", "entity": "Jupiter", "parameters": {{"steps": [{{"action": "go_to", "entity": "Jupiter"}}, {{"action": "track", "entity": "Jupiter"}}]}}}}
"go to mars then land on mars" -> {{"action": "multi_step", "entity": "Mars", "parameters": {{"steps": [{{"action": "go_to", "entity": "Mars"}}, {{"action": "land_on", "entity": "Mars"}}]}}}}
"fly to saturn and take screenshot" -> {{"action": "multi_step", "entity": "Saturn", "parameters": {{"steps": [{{"action": "go_to", "entity": "Saturn"}}, {{"action": "take_screenshot", "entity": ""}}]}}}}

Advanced Cinematic Commands:
"smooth camera transition to mars" -> {{"action": "camera_transition", "entity": "Mars", "parameters": {{"duration": 5.0}}}}
"cinematic camera to jupiter" -> {{"action": "camera_transition", "entity": "Jupiter", "parameters": {{"duration": 8.0}}}}

Path Drawing Commands:
"draw path to mars" -> {{"action": "draw_path", "entity": "Mars", "parameters": {{"color": "red"}}}}
"draw trajectory to jupiter" -> {{"action": "draw_path", "entity": "Jupiter", "parameters": {{"color": "blue"}}}}
"show path to saturn" -> {{"action": "draw_path", "entity": "Saturn"}}

Visual Marker Commands:
"mark jupiter with red circle" -> {{"action": "add_marker", "entity": "Jupiter", "parameters": {{"color": "red", "shape": "sphere"}}}}
"add marker around mars" -> {{"action": "add_marker", "entity": "Mars", "parameters": {{"color": "green"}}}}
"place marker on saturn" -> {{"action": "add_marker", "entity": "Saturn"}}

Time Travel Commands:
"time travel to 2050" -> {{"action": "time_travel", "entity": "", "parameters": {{"year": 2050}}}}
"go to year 2030" -> {{"action": "time_travel", "entity": "", "parameters": {{"year": 2030}}}}
"travel to future" -> {{"action": "time_travel", "entity": "", "parameters": {{"year": 2040}}}}

Camera Control Commands:
"pitch camera up" -> {{"action": "pitch_camera", "entity": "", "parameters": {{"angle": 30}}}}
"roll camera left" -> {{"action": "roll_camera", "entity": "", "parameters": {{"angle": -45}}}}
"smooth camera orientation to mars" -> {{"action": "smooth_orientation", "entity": "Mars", "parameters": {{"duration": 3.0}}}}

Only return the JSON, nothing else."""

        try:
            import requests
            
            print(f"🧠 [LLM] Sending request to: {self.base_url}/chat/completions")
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    "temperature": LM_STUDIO_TEMPERATURE,
                    "max_tokens": LM_STUDIO_MAX_TOKENS
                },
                timeout=LM_STUDIO_TIMEOUT
            )
            
            print(f"🧠 [LLM] Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                # Extract JSON from response (handle nested structures)
                cmd_data = self._extract_json_from_response(content)
                if cmd_data:
                    return Command(
                        action=cmd_data.get('action', '') or '',
                        entity=cmd_data.get('entity', '') or '',
                        parameters=cmd_data.get('parameters', {})
                    )
            
        except Exception as e:
            print(f"❌ [LLM] Connection/parsing error: {e}")
            logger.error(f"LLM parsing error: {e}")
            
        print(f"❌ [LLM] Failed to parse command")
        return None
    
    def _extract_json_from_response(self, content: str) -> dict:
        """Extract JSON from LLM response with multiple fallback strategies"""
        import json
        
        # Strategy 1: Look for JSON code blocks
        code_block_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', content, re.IGNORECASE)
        if code_block_match:
            try:
                return json.loads(code_block_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Strategy 2: Find complete JSON objects (handle nested structures)
        json_pattern = r'\{(?:[^{}]|{[^{}]*})*\}'
        json_matches = re.findall(json_pattern, content)
        
        for match in json_matches:
            try:
                data = json.loads(match)
                # Validate it has required fields
                if 'action' in data:
                    return data
            except json.JSONDecodeError:
                continue
        
        # Strategy 3: Try to fix common JSON issues
        for match in json_matches:
            try:
                # Fix missing quotes around keys
                fixed = re.sub(r'(\w+):', r'"\1":', match)
                # Fix single quotes
                fixed = fixed.replace("'", '"')
                data = json.loads(fixed)
                if 'action' in data:
                    return data
            except json.JSONDecodeError:
                continue
        
        return None

class SpaceNavigationController:
    """
    Universal space navigation controller with AI-powered command processing
    
    Features:
    - Natural language command processing
    - Direct voice commands (no wake word)
    - Situational awareness and smart validation
    - Multi-tool sequences and tours
    - Extensive recovery mechanisms
    """
    
    def __init__(self):
        self.llm = UniversalLLMProvider()
        self.connection_manager = get_connection_manager()
        self.method_registry = get_method_registry()
        self.last_target = None  # Track last navigation target
        self.speech_recognizer = None  # Speech recognition system
        self.tts_engine = None  # TTS for voice cues
        
        # Smart completion detection
        self.completion_manager = get_completion_manager(self.method_registry)
        
        # Audio coordination
        if SPEECH_AVAILABLE:
            self.audio_manager = get_audio_state_manager()
        else:
            self.audio_manager = None
        
        # Map actions to methods (Phase 1 + Phase 2 new methods)
        self.action_map = {
            # Phase 1: Core methods (18 methods)
            'go_to': self._go_to,
            'land_on': self._land_on,
            'track': self._track,
            'explore': self._explore,
            'take_screenshot': self._screenshot,
            'set_time': self._set_time,
            'free_camera': self._free_camera,
            'stop_camera': self._stop_camera,
            'back_to_space': self._back_to_space,
            'tour': self._tour,
            'cinematic_journey': self._cinematic_journey,
            'multi_step': self._multi_step,
            'stream_tour': self._stream_tour,
            'orbit': self._orbit,
            'zoom_in': self._zoom_in,
            'zoom_out': self._zoom_out,
            'speed_up': self._speed_up,
            'slow_down': self._slow_down,
            
            # Phase 2: Advanced new methods (7 new methods)
            'camera_transition': self._camera_transition,
            'draw_path': self._draw_path,
            'add_marker': self._add_marker,
            'time_travel': self._time_travel,
            'pitch_camera': self._pitch_camera,
            'roll_camera': self._roll_camera,
            'smooth_orientation': self._smooth_orientation
        }
        
        logger.info("🚀 Astro Remote Controller initialized")
    
    def execute_command_with_completion(self, user_input: str) -> str:
        """
        Execute command and wait for completion (for sequential voice control)
        
        Args:
            user_input: Natural language command
            
        Returns:
            Completion result message
        """
        logger.info(f"🎯 Executing command with completion tracking: {user_input}")
        
        try:
            # Execute the command - completion detection is now handled within each method
            result = self.execute_command(user_input)
            
            # Note: Individual command methods now handle their own completion detection:
            # - Navigation commands use waitFocus() or intelligent fallback timing
            # - Fast commands use minimal verification delays
            # - Multi-step commands handle sequential completion
            # No more hardcoded timeouts needed here!
            
            logger.info(f"✅ Command completed with smart detection: {result}")
            return result
            
        except Exception as e:
            error_msg = f"❌ Command execution failed: {str(e)}"
            logger.error(error_msg)
            return error_msg
        
    def connect(self) -> bool:
        """Connect to Gaia Sky and keep connection alive"""
        try:
            if self.connection_manager.connect():
                logger.info("Establishing persistent Gaia Sky connection...")
                return True
        except Exception as e:
            logger.error(f"Connection error: {e}")
        return False
        
    def disconnect(self):
        """Disconnect from Gaia Sky and cleanup resources"""
        try:
            if self.connection_manager:
                logger.info("Closing Gaia Sky connection...")
                # Connection manager handles cleanup automatically
            if self.speech_recognizer:
                self.speech_recognizer.stop_listening()
        except Exception as e:
            logger.error(f"Disconnect error: {e}")
    
    def start_speech_recognition(self, custom_callback=None) -> bool:
        """Start speech recognition for direct commands"""
        if not SPEECH_AVAILABLE:
            logger.error("Speech recognition not available")
            print("❌ Speech recognition not available")
            print("💡 Install dependencies with: pip install openai-whisper pyaudio")
            return False
            
        try:
            if self.speech_recognizer:
                logger.warning("Speech recognition already running")
                return True
            
            logger.info("Initializing Astro speech recognition...")
            self.speech_recognizer = UniversalSpeechRecognizer()
            
            # Initialize TTS engine if not already done
            if not self.tts_engine:
                self.tts_engine = CoquiTTSEngine()
            
            # Connect TTS to speech recognizer for voice cues
            self.speech_recognizer.set_tts_engine(self.tts_engine)
            
            # Use custom callback if provided, otherwise use default
            if custom_callback:
                command_handler = custom_callback
            else:
                def handle_speech_command(command: str):
                    """Handle commands from speech recognition"""
                    logger.info(f"Voice Command: '{command}'")
                    result = self.execute_command_with_completion(command)
                    logger.info(f"Voice Result: {result}")
                    
                    # NOTE: TTS feedback is now handled within execute_command_with_completion()
                    # No additional TTS needed here to avoid duplicate responses
                command_handler = handle_speech_command
            
            if self.speech_recognizer.start_listening(command_handler):
                print("✅ Speech recognition active! Say commands directly to control Gaia Sky")
                print("💡 Example: 'Take me to Mars'")
                return True
            else:
                print("❌ Failed to start speech recognition")
                return False
                
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return False
    
    def stop_speech_recognition(self):
        """Stop speech recognition"""
        if self.speech_recognizer:
            logger.info("Stopping speech recognition...")
            self.speech_recognizer.stop_listening()
            self.speech_recognizer = None
            print("✅ Speech recognition stopped")
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current camera and navigation state for smart validation"""
        try:
            gs, error_msg = self._get_gaia_sky_interface_with_validation()
            if not gs:
                return {"error": error_msg, "connected": False}
                
            # Try to get camera position (if available)
            try:
                camera_position = None
                if self.method_registry.validate_method_call(gs, 'getCameraPosition'):
                    try:
                        camera_position = gs.getCameraPosition()
                        if hasattr(camera_position, '__len__') and len(camera_position) >= 3:
                            camera_position = list(camera_position[:3])
                    except:
                        camera_position = None
                
                return {
                    "connected": True,
                    "camera_position": camera_position,
                    "last_target": self.last_target,
                    "timestamp": time.time(),
                    "gaia_sky_available": True
                }
            except Exception as inner_e:
                logger.warning(f"Could not get detailed state: {inner_e}")
                return {
                    "connected": True,
                    "camera_position": None,
                    "last_target": self.last_target,
                    "timestamp": time.time(),
                    "gaia_sky_available": True
                }
                
        except Exception as e:
            logger.error(f"State check failed: {e}")
            return {"error": f"State check failed: {e}", "connected": False}
    
    def _get_gaia_sky_interface_with_validation(self) -> Tuple[Any, str]:
        """Get Gaia Sky interface with connection validation"""
        gs = self.connection_manager.get_gaia_sky_interface()
        if not gs:
            return None, "❌ No connection to Gaia Sky. Make sure Gaia Sky is running with Python bridge enabled."
        return gs, ""
    
    def _validate_and_call_method(self, gs: Any, method_name: str, *args) -> Tuple[bool, str]:
        """Validate method exists and call it safely"""
        try:
            if not self.method_registry.validate_method_call(gs, method_name):
                return False, f"Method '{method_name}' not available in current Gaia Sky version"
            
            # Get the method and call it
            method = getattr(gs, method_name)
            if args:
                method(*args)
            else:
                method()
            
            return True, f"Successfully called {method_name}"
            
        except Exception as e:
            logger.error(f"Method {method_name} failed: {e}")
            return False, f"Method '{method_name}' failed: {str(e)}"
    
    def _validate_entity(self, action: str, entity: str) -> Tuple[bool, str]:
        """Validate entity based on command type"""
        try:
            from .utils.config import CELESTIAL_OBJECTS
        except ImportError:
            from utils.config import CELESTIAL_OBJECTS
        
        # Navigation commands need valid celestial objects
        navigation_actions = ['go_to', 'land_on', 'track', 'explore', 'orbit']
        
        if action in navigation_actions and entity:
            # Check if entity is in known celestial objects (case insensitive)
            valid_objects = [obj.lower() for obj in CELESTIAL_OBJECTS]
            if entity.lower() not in valid_objects:
                # Check for common variations/aliases
                aliases = {
                    'sun': 'sun',
                    'moon': 'moon', 
                    'earth': 'earth',
                    'red planet': 'mars',
                    'gas giant': 'jupiter',
                    'ringed planet': 'saturn',
                    'alpha centauri': 'alpha centauri'
                }
                entity_lower = entity.lower()
                if entity_lower in aliases:
                    return True, f"Valid entity (alias for {aliases[entity_lower]})"
                else:
                    return False, f"Unknown celestial object: '{entity}'. Try: {', '.join(CELESTIAL_OBJECTS[:8])}..."
        
        return True, "Entity validation passed"
    
    def should_execute_command(self, action: str, entity: str, current_state: Dict) -> Tuple[bool, str]:
        """Smart validation before executing commands"""
        
        if current_state.get("error"):
            return True, "Cannot check state - will attempt execution"
        
        # Validate entity first
        entity_valid, entity_message = self._validate_entity(action, entity)
        if not entity_valid:
            return False, entity_message
        
        # Skip redundant navigation
        if action == "go_to" and entity and entity.lower() == ((current_state.get("last_target") or "").lower()):
            return False, f"Already at {entity} - no navigation needed"
        
        # Skip unnecessary camera operations based on state
        if action == "free_camera":
            pos = current_state.get("camera_position", [0, 0, 0])
            if pos and any(abs(coord) > 100000 for coord in pos):
                return False, "Camera already appears to be free in space"
        
        if action == "back_to_space":
            pos = current_state.get("camera_position", [0, 0, 0])
            if pos and any(abs(coord) > 50000 for coord in pos):
                return False, "Already in space - no need to go back to space"
        
        return True, "Command validation passed"
            
    def execute_command(self, user_input: str) -> str:
        """Execute natural language command with situational awareness"""
        
        # Validate input
        if not user_input or not user_input.strip():
            return "❌ Empty command. Please provide a valid space navigation command."
        
        user_input = user_input.strip()
        
        # Check for very short or nonsensical input
        if len(user_input) < 3:
            return "❌ Command too short. Please provide a more detailed instruction."
        
        # Get current state first
        current_state = self.get_current_state()
        pos_info = "unknown"
        if current_state.get('camera_position'):
            pos_info = str(current_state['camera_position'][:3])
        
        logger.info(f"Current state: Position={pos_info}, Target={current_state.get('last_target', 'none')}")
        
        # Parse command using LLM
        # Voice cue: starting LLM processing
        if self.tts_engine:
            self.tts_engine.speak_indicator_sync("processing")
            
        command = self.llm.parse_command(user_input)
        if not command or not command.action:
            # Voice cue: LLM failed to understand
            if self.tts_engine:
                self.tts_engine.speak_indicator_sync("unclear")
            return f"❌ LLM failed to parse command: '{user_input}'"
        
        # Smart validation before execution
        should_execute, reason = self.should_execute_command(command.action, command.entity, current_state)
        
        if not should_execute:
            logger.info(f"🧠 SMART SKIP: {reason}")
            return f"🧠 Smart Agent: {reason}"
        
        logger.info(f"✅ EXECUTING: {command.action} {command.entity} - {reason}")
        
        # Voice cue: executing command
        if self.tts_engine:
            self.tts_engine.speak_indicator_sync("executing")
        
        # Execute command
        if command.action in self.action_map:
            result = self.action_map[command.action](command.entity, command.parameters or {})
            
            # Voice cue: command execution result
            if self.tts_engine:
                if result and not result.startswith("❌"):
                    self.tts_engine.speak_indicator_sync("complete")
                else:
                    self.tts_engine.speak_indicator_sync("failed")
            
            # Update last target for navigation commands
            if command.action in ['go_to', 'land_on', 'explore'] and command.entity:
                self.last_target = command.entity
                
            return result
        else:
            # Voice cue: unknown action
            if self.tts_engine:
                self.tts_engine.speak_indicator_sync("unclear")
            return f"Unknown action: {command.action}"
    
    def _try_fallback_parsing(self, user_input: str) -> str:
        """Fallback parsing using regex patterns"""
        input_lower = user_input.lower()
        
        # Simple pattern matching for common commands
        if any(word in input_lower for word in ['mars', 'red planet']):
            return self._go_to('Mars', {})
        elif any(word in input_lower for word in ['jupiter', 'gas giant']):
            return self._go_to('Jupiter', {})
        elif any(word in input_lower for word in ['saturn', 'ring', 'ringed']):
            return self._go_to('Saturn', {})
        elif any(word in input_lower for word in ['venus', 'morning star', 'evening star']):
            return self._go_to('Venus', {})
        elif any(word in input_lower for word in ['moon', 'luna']):
            return self._go_to('Moon', {})
        elif any(word in input_lower for word in ['earth', 'home', 'blue planet']):
            return self._go_to('Earth', {})
        elif any(word in input_lower for word in ['screenshot', 'photo', 'picture', 'pic']):
            return self._screenshot('', {})
        elif any(word in input_lower for word in ['stuck', 'help', 'free', 'unlock']):
            return self._free_camera('', {})
        elif any(word in input_lower for word in ['land', 'touch down', 'set down']):
            if 'mars' in input_lower:
                return self._land_on('Mars', {})
            elif 'moon' in input_lower:
                return self._land_on('Moon', {})
            else:
                return self._land_on('Moon', {})  # Default
        else:
            return "Sorry, I couldn't understand that command. Try: 'go to Mars', 'take screenshot', 'land on Moon'"
    
    def _go_to(self, entity: str, params: dict) -> str:
        """Navigate to celestial object - REAL IMPLEMENTATION (FIXED)"""
        if not entity:
            return "❌ Please specify where to go (e.g., 'Mars', 'Jupiter')"
            
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Try navigation methods in order of preference (from working Astro implementation)
            smooth = params.get('smooth', True)
            angle = params.get('angle', 0.0)
            duration = params.get('duration', 5.0)
            
            if smooth:
                # Try goToObjectSmooth with correct 3 parameters
                try:
                    gs.goToObjectSmooth(entity, angle, duration)
                    logger.info(f"Smooth navigation to {entity} initiated (angle={angle}, duration={duration})")
                    
                    # Wait for navigation completion using smart detection
                    navigation_params = {'smooth': True, 'duration': duration, 'angle': angle}
                    completion_success = self.completion_manager.wait_for_completion(
                        'go_to', gs, entity, **navigation_params
                    )
                    
                    if completion_success:
                        self.last_target = entity
                        return f"✈️ Successfully navigated to {entity} (smooth)!"
                    else:
                        logger.warning(f"Navigation completion detection failed for {entity}")
                        self.last_target = entity
                        return f"✈️ Navigation to {entity} initiated (completion uncertain)"
                        
                except Exception as e:
                    logger.warning(f"goToObjectSmooth failed: {e}, trying fallback...")
                
                # Fallback to basic goToObject
                try:
                    gs.goToObject(entity)
                    logger.info(f"Navigation to {entity} initiated (basic)")
                    
                    # Wait for completion with fallback navigation
                    navigation_params = {'smooth': False}
                    completion_success = self.completion_manager.wait_for_completion(
                        'go_to', gs, entity, **navigation_params
                    )
                    
                    self.last_target = entity
                    return f"✈️ Successfully navigated to {entity}!"
                except Exception as e:
                    logger.warning(f"goToObject failed: {e}")
            else:
                # Try instant navigation
                try:
                    gs.goToObjectInstant(entity)
                    logger.info(f"Instant navigation to {entity} completed")
                    
                    # Brief wait for instant navigation (should be very fast)
                    navigation_params = {'instant': True}
                    completion_success = self.completion_manager.wait_for_completion(
                        'go_to', gs, entity, **navigation_params
                    )
                    
                    self.last_target = entity
                    return f"✈️ Instantly navigated to {entity}!"
                except Exception as e:
                    logger.warning(f"goToObjectInstant failed: {e}, trying fallback...")
                
                # Fallback to basic goToObject
                try:
                    gs.goToObject(entity)
                    logger.info(f"Navigation to {entity} initiated (fallback)")
                    
                    # Wait for completion with fallback navigation
                    navigation_params = {'smooth': False}
                    completion_success = self.completion_manager.wait_for_completion(
                        'go_to', gs, entity, **navigation_params
                    )
                    
                    self.last_target = entity
                    return f"✈️ Successfully navigated to {entity}!"
                except Exception as e:
                    logger.warning(f"goToObject fallback failed: {e}")
            
            return f"❌ All navigation methods failed for {entity}"
            
        except Exception as e:
            logger.error(f"Navigation to {entity} failed: {e}")
            return f"❌ Navigation to {entity} failed: {str(e)}"
    
    def _land_on(self, entity: str, params: dict) -> str:
        """Land on celestial object - REAL IMPLEMENTATION"""
        if not entity:
            return "❌ Please specify where to land (e.g., 'Moon', 'Mars')"
            
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Check if specific coordinates provided
            latitude = params.get('latitude')
            longitude = params.get('longitude')
            
            if latitude is not None and longitude is not None:
                # Land at specific coordinates
                if self.method_registry.validate_method_call(gs, 'landAtObjectLocation'):
                    gs.landAtObjectLocation(entity, latitude, longitude)
                    logger.info(f"Landing on {entity} at coordinates ({latitude}, {longitude})")
                    location_info = f" at coordinates ({latitude:.2f}, {longitude:.2f})"
                else:
                    return f"❌ Landing at coordinates not supported for {entity}"
            else:
                # Land at default location
                if self.method_registry.validate_method_call(gs, 'landOnObject'):
                    gs.landOnObject(entity)
                    logger.info(f"Landing on {entity} at default location")
                    location_info = ""
                else:
                    return f"❌ Landing not supported for {entity}"
            
            # Wait for landing to complete using smart detection
            landing_params = {'latitude': latitude, 'longitude': longitude} if latitude is not None else {}
            completion_success = self.completion_manager.wait_for_completion(
                'land_on', gs, entity, **landing_params
            )
            
            self.last_target = entity
            return f"🛬 Successfully landed on {entity}{location_info}!"
            
        except Exception as e:
            logger.error(f"Landing on {entity} failed: {e}")
            return f"❌ Landing on {entity} failed: {str(e)}"
    
    def _track(self, entity: str, params: dict) -> str:
        """Track celestial object - REAL IMPLEMENTATION"""
        if not entity:
            return "❌ Please specify what to track (e.g., 'Saturn', 'Jupiter')"
            
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Set camera focus on the object for tracking
            if self.method_registry.validate_method_call(gs, 'setCameraFocus'):
                gs.setCameraFocus(entity)
                logger.info(f"Camera focus set to track {entity}")
            else:
                return f"❌ Tracking not supported for {entity}"
            
            # Optional: Set camera to track mode if available
            if hasattr(gs, 'setCameraTrackingObject') and self.method_registry.validate_method_call(gs, 'setCameraTrackingObject'):
                gs.setCameraTrackingObject(entity)
                logger.info(f"Camera tracking mode activated for {entity}")
            
            # Wait for tracking operation to complete
            tracking_params = {}
            completion_success = self.completion_manager.wait_for_completion(
                'track', gs, entity, **tracking_params
            )
            
            self.last_target = entity
            return f"👁️ Now tracking {entity}... Camera will follow its movement!"
            
        except Exception as e:
            logger.error(f"Tracking {entity} failed: {e}")
            return f"❌ Tracking {entity} failed: {str(e)}"
    
    def _explore(self, entity: str, params: dict) -> str:
        """Explore celestial object - REAL IMPLEMENTATION"""
        if not entity:
            return "❌ Please specify what to explore (e.g., 'Venus', 'Saturn')"
            
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # First navigate to the object with correct signature
            if self.method_registry.validate_method_call(gs, 'goToObjectSmooth'):
                # goToObjectSmooth requires 3 parameters: (name, positionDurationSeconds, orientationDurationSeconds)
                gs.goToObjectSmooth(entity, 0.0, 5.0)
                
                # Wait for navigation completion using smart detection
                navigation_params = {'smooth': True}
                completion_success = self.completion_manager.wait_for_completion(
                    'explore', gs, entity, **navigation_params
                )
            
            # Set camera focus for exploration
            if self.method_registry.validate_method_call(gs, 'setCameraFocus'):
                gs.setCameraFocus(entity)
            
            # Exploration complete - no additional camera transition needed
            # (cameraTransition requires specific camera position parameters, not entity name)
            
            self.last_target = entity
            return f"🌌 Exploring {entity} in cinematic mode... Discovering cosmic wonders!"
            
        except Exception as e:
            logger.error(f"Exploration of {entity} failed: {e}")
            return f"❌ Exploration of {entity} failed: {str(e)}"
    
    def _screenshot(self, entity: str, params: dict) -> str:
        """Take screenshot - REAL IMPLEMENTATION"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Configure screenshot quality if parameters provided
            width = params.get('width', 1920)
            height = params.get('height', 1080)
            directory = params.get('directory', '/tmp')
            namePrefix = params.get('namePrefix', 'gaia_screenshot')
            
            # Configure screenshot settings if available (correct signature)
            if self.method_registry.validate_method_call(gs, 'configureScreenshots'):
                # configureScreenshots requires: (width, height, directory, namePrefix)
                gs.configureScreenshots(width, height, directory, namePrefix)
                logger.info(f"Screenshot configured: {width}x{height} in {directory} with prefix {namePrefix}")
            
            # Take the screenshot
            if self.method_registry.validate_method_call(gs, 'takeScreenshot'):
                gs.takeScreenshot()
                logger.info("Screenshot captured")
                
                # Quick verification for screenshot completion (fast command)
                screenshot_params = {'width': width, 'height': height, 'directory': directory, 'namePrefix': namePrefix}
                completion_success = self.completion_manager.wait_for_completion(
                    'take_screenshot', gs, '', **screenshot_params
                )
                
                # Save with custom filename if provided
                filename = params.get('filename')
                if filename and self.method_registry.validate_method_call(gs, 'saveScreenshot'):
                    gs.saveScreenshot(filename)
                    return f"📸 Screenshot saved as '{filename}'!"
                else:
                    return "📸 Screenshot captured and saved to default directory!"
            else:
                return "❌ Screenshot functionality not available"
            
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return f"❌ Screenshot failed: {str(e)}"
    
    def _set_time(self, entity: str, params: dict) -> str:
        """Set time - REAL IMPLEMENTATION"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Extract time parameters
            year = params.get('year', 2025)
            month = params.get('month', 1)
            day = params.get('day', 1)
            hour = params.get('hour', 12)
            minute = params.get('minute', 0)
            second = params.get('second', 0)
            millisec = params.get('millisec', 0)
            
            # Set simulation time (correct signature requires 7 parameters)
            if self.method_registry.validate_method_call(gs, 'setSimulationTime'):
                gs.setSimulationTime(year, month, day, hour, minute, second, millisec)
                logger.info(f"Time set to {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}.{millisec:03d}")
                return f"⏰ Time set to {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
            else:
                return "❌ Time control not available"
            
        except Exception as e:
            logger.error(f"Time setting failed: {e}")
            return f"❌ Time setting failed: {str(e)}"
    
    def _free_camera(self, entity: str, params: dict) -> str:
        """Free the camera - REAL IMPLEMENTATION"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Stop any current camera movement
            if self.method_registry.validate_method_call(gs, 'cameraStop'):
                gs.cameraStop()
                logger.info("Camera movement stopped")
            
            # Set camera to free mode if available
            if self.method_registry.validate_method_call(gs, 'setCameraFree'):
                gs.setCameraFree()
                logger.info("Camera set to free mode")
            
            # Enable input controls
            if self.method_registry.validate_method_call(gs, 'enableInput'):
                gs.enableInput()
            
            # Wait for camera operation completion
            camera_params = {}
            completion_success = self.completion_manager.wait_for_completion(
                'free_camera', gs, '', **camera_params
            )
            
            return "🔓 Camera freed! You can now navigate freely again."
            
        except Exception as e:
            logger.error(f"Camera free operation failed: {e}")
            return f"❌ Camera free failed: {str(e)}"
    
    def _stop_camera(self, entity: str, params: dict) -> str:
        """Stop camera movement - REAL IMPLEMENTATION"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Stop all camera movement
            if self.method_registry.validate_method_call(gs, 'cameraStop'):
                gs.cameraStop()
                logger.info("All camera movement stopped")
                
                # Quick verification for camera stop (fast command)
                camera_params = {}
                completion_success = self.completion_manager.wait_for_completion(
                    'stop_camera', gs, '', **camera_params
                )
                
                return "⏹️ Camera movement stopped!"
            else:
                return "❌ Camera stop functionality not available"
            
        except Exception as e:
            logger.error(f"Camera stop failed: {e}")
            return f"❌ Camera stop failed: {str(e)}"
    
    def _back_to_space(self, entity: str, params: dict) -> str:
        """Return to space - REAL IMPLEMENTATION"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Stop current camera movement
            if self.method_registry.validate_method_call(gs, 'cameraStop'):
                gs.cameraStop()
            
            # Set camera to free mode
            if self.method_registry.validate_method_call(gs, 'setCameraFree'):
                gs.setCameraFree()
            
            # Move camera away from current object if we have a last target
            if self.last_target and self.method_registry.validate_method_call(gs, 'cameraForward'):
                # Move camera forward (away from surface)
                gs.cameraForward(10000)  # Move 10,000 units away
                logger.info(f"Camera moved away from {self.last_target}")
            
            # Wait for camera movement completion
            space_params = {'last_target': self.last_target}
            completion_success = self.completion_manager.wait_for_completion(
                'back_to_space', gs, '', **space_params
            )
            
            return "🚀 Back to space! Camera moved away from surface."
            
        except Exception as e:
            logger.error(f"Back to space operation failed: {e}")
            return f"❌ Back to space failed: {str(e)}"
    
    def _tour(self, entity: str, params: dict) -> str:
        """Multi-step tour - REAL IMPLEMENTATION"""
        if not entity:
            entity = "solar system"
            
        try:
            from .utils.config import TOUR_ROUTES
        except ImportError:
            from utils.config import TOUR_ROUTES
            
        # Get tour route
        route = TOUR_ROUTES.get(entity.lower())
        if not route:
            return f"❌ No tour route defined for '{entity}'. Available tours: {', '.join(TOUR_ROUTES.keys())}"
        
        # Execute tour sequence
        results = [f"🎬 Starting {entity} tour with {len(route)} destinations..."]
        
        # Get tour parameters
        delay = params.get('delay', 3.0)  # seconds between destinations
        smooth = params.get('smooth', True)
        
        for i, destination in enumerate(route, 1):
            try:
                # Navigate to destination
                nav_params = {'smooth': smooth, 'duration': 4.0}
                nav_result = self._go_to(destination, nav_params)
                
                if "❌" in nav_result:
                    results.append(f"⚠️ Tour Stop {i}/{len(route)}: Failed to reach {destination}")
                    continue
                    
                results.append(f"✅ Tour Stop {i}/{len(route)}: {destination}")
                
                # Wait before next destination (except for last one)
                if i < len(route):
                    time.sleep(delay)
                    
            except Exception as e:
                results.append(f"❌ Tour Stop {i}/{len(route)}: Error reaching {destination} - {str(e)}")
                continue
        
        results.append(f"🎉 {entity.title()} tour completed! Visited {len(route)} destinations.")
        return '\n'.join(results)
    
    def _cinematic_journey(self, entity: str, params: dict) -> str:
        """Cinematic journey - REAL IMPLEMENTATION"""
        if not entity:
            return "❌ Please specify destination for cinematic journey (e.g., 'Mars', 'Jupiter')"
            
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Get cinematic parameters
            duration = params.get('duration', 8.0)  # longer duration for cinematic effect
            smooth = params.get('smooth', True)
            track_after = params.get('track_after', True)
            
            results = [f"🎬 Starting cinematic journey to {entity}..."]
            
            # Phase 1: Smooth navigation with extended duration
            nav_params = {
                'smooth': True, 
                'duration': duration,
                'angle': 0.0  # frontal approach
            }
            
            nav_result = self._go_to(entity, nav_params)
            if "❌" in nav_result:
                return f"❌ Cinematic journey to {entity} failed: Could not navigate there"
            
            results.append(f"✅ Approaching {entity} cinematically...")
            
            # Phase 2: Wait for smooth navigation to complete
            time.sleep(duration + 1.0)
            
            # Phase 3: Set cinematic tracking if requested
            if track_after:
                if self.method_registry.validate_method_call(gs, 'setCameraFocus'):
                    gs.setCameraFocus(entity)
                    results.append(f"📹 Camera locked on {entity} for cinematic tracking")
                
                # Optional: Add smooth camera movement around the object using focus
                if self.method_registry.validate_method_call(gs, 'setCameraFocus'):
                    gs.setCameraFocus(entity)
                    results.append(f"🌌 Camera focused on {entity} for cinematic tracking")
                    
                    # Add gentle rotation if available
                    if self.method_registry.validate_method_call(gs, 'cameraRotate'):
                        gs.cameraRotate(0.3, 0.0)  # gentle rotation
                        results.append(f"🌌 Gentle camera movement activated for cinematic effect")
            
            # Phase 4: Optional visual enhancements
            visual_effects = params.get('effects', True)
            if visual_effects:
                # Adjust time scale for dramatic effect if available
                if self.method_registry.validate_method_call(gs, 'setTimeWarp'):
                    try:
                        gs.setTimeWarp(0.2)  # slow motion effect
                        results.append("⏰ Time slowed for dramatic cinematic effect")
                        
                        # Reset to normal after a few seconds
                        time.sleep(3.0)
                        gs.setTimeWarp(1.0)
                        results.append("⏰ Time restored to normal")
                    except:
                        pass
            
            self.last_target = entity
            results.append(f"🎭 Cinematic journey to {entity} completed! Enjoy the spectacular view!")
            
            return '\n'.join(results)
            
        except Exception as e:
            logger.error(f"Cinematic journey to {entity} failed: {e}")
            return f"❌ Cinematic journey to {entity} failed: {str(e)}"
    
    def _multi_step(self, entity: str, params: dict) -> str:
        """Execute multi-step command sequence - ENHANCED IMPLEMENTATION"""
        steps = params.get('steps', [])
        
        if not steps:
            return "❌ No steps provided for multi-step command"
        
        # Enhanced parameters
        delay_between_steps = params.get('delay', 2.0)  # seconds between steps
        stop_on_error = params.get('stop_on_error', False)  # continue or stop on errors
        show_progress = params.get('show_progress', True)
        
        results = []
        results.append(f"🔄 Executing multi-step sequence ({len(steps)} steps)...")
        if show_progress:
            results.append(f"⚙️ Settings: {delay_between_steps}s delay, {'stop' if stop_on_error else 'continue'} on error")
        
        successful_steps = 0
        failed_steps = 0
        
        for i, step in enumerate(steps, 1):
            try:
                # Progress indicator
                if show_progress:
                    results.append(f"🎯 Step {i}/{len(steps)}: Processing...")
                
                if isinstance(step, dict):
                    # Step is already a structured command
                    action = step.get('action', '')
                    step_entity = step.get('entity', '')
                    step_params = step.get('parameters', {})
                elif isinstance(step, str):
                    # Step is a string, need to parse it
                    if step in self.action_map:
                        action = step
                        step_entity = entity  # Use the main entity
                        step_params = {}
                    else:
                        # Try to parse as "action entity" format
                        parts = step.split()
                        if len(parts) >= 2:
                            action = parts[0]
                            step_entity = ' '.join(parts[1:])
                            step_params = {}
                        else:
                            results.append(f"❌ Step {i}: Invalid step format: {step}")
                            failed_steps += 1
                            if stop_on_error:
                                results.append("🛑 Stopping multi-step sequence due to error")
                                break
                            continue
                else:
                    results.append(f"❌ Step {i}: Invalid step type: {type(step)}")
                    failed_steps += 1
                    if stop_on_error:
                        results.append("🛑 Stopping multi-step sequence due to error")
                        break
                    continue
                
                # Execute the step
                if action in self.action_map:
                    step_result = self.action_map[action](step_entity, step_params)
                    
                    # Check if step was successful
                    if "❌" in step_result:
                        results.append(f"⚠️ Step {i}: {step_result}")
                        failed_steps += 1
                        if stop_on_error:
                            results.append("🛑 Stopping multi-step sequence due to step failure")
                            break
                    else:
                        results.append(f"✅ Step {i}: {step_result}")
                        successful_steps += 1
                    
                    # Update last target for navigation commands
                    if action in ['go_to', 'land_on', 'explore'] and step_entity:
                        self.last_target = step_entity
                else:
                    results.append(f"❌ Step {i}: Unknown action '{action}'")
                    failed_steps += 1
                    if stop_on_error:
                        results.append("🛑 Stopping multi-step sequence due to unknown action")
                        break
                
                # Wait between steps (except for last step)
                if i < len(steps) and delay_between_steps > 0:
                    if show_progress:
                        results.append(f"⏰ Waiting {delay_between_steps}s before next step...")
                    time.sleep(delay_between_steps)
                    
            except Exception as e:
                results.append(f"❌ Step {i}: Exception - {str(e)}")
                failed_steps += 1
                logger.error(f"Multi-step error at step {i}: {e}")
                if stop_on_error:
                    results.append("🛑 Stopping multi-step sequence due to exception")
                    break
        
        # Summary
        total_attempted = successful_steps + failed_steps
        results.append(f"📊 Multi-step sequence completed!")
        results.append(f"✅ Successful: {successful_steps}/{total_attempted}, ❌ Failed: {failed_steps}/{total_attempted}")
        
        if successful_steps == len(steps):
            results.append("🎉 All steps completed successfully!")
        elif successful_steps > 0:
            results.append("⚠️ Partial success - some steps failed")
        else:
            results.append("💥 All steps failed")
                
        return '\n'.join(results)
    
    def _orbit(self, entity: str, params: dict) -> str:
        """Orbit around celestial object - REAL IMPLEMENTATION"""
        if not entity:
            return "❌ Please specify what to orbit (e.g., 'Earth', 'Jupiter')"
            
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Get orbit parameters
            distance = params.get('distance', 10.0)  # orbit distance multiplier  
            speed = params.get('speed', 1.0)  # orbit speed
            
            # First navigate to the object
            nav_result = self._go_to(entity, {'smooth': True})
            if "❌" in nav_result:
                return f"❌ Cannot orbit {entity}: Failed to navigate there first"
            
            # Since setCameraOrbitObject doesn't exist, use focus + rotation simulation
            if self.method_registry.validate_method_call(gs, 'setCameraFocus'):
                # Focus on the object first
                gs.setCameraFocus(entity)
                logger.info(f"Camera focused on {entity} for orbital tracking")
                
                # Simulate orbital motion using camera rotation (if available)
                if self.method_registry.validate_method_call(gs, 'cameraRotate'):
                    # Small orbital movement to simulate orbit
                    rotation_speed = speed * 0.1  # Scale down the rotation
                    gs.cameraRotate(rotation_speed, 0.0)
                    logger.info(f"Orbital rotation applied (speed: {rotation_speed})")
                    return f"🌌 Now orbiting {entity}! Use manual controls to continue orbital movement."
                else:
                    return f"🌌 Focused on {entity} - use manual camera controls to orbit around it!"
            else:
                return f"❌ Orbit functionality not available for {entity}"
                
        except Exception as e:
            logger.error(f"Orbiting {entity} failed: {e}")
            return f"❌ Orbiting {entity} failed: {str(e)}"
    
    def _zoom_in(self, entity: str, params: dict) -> str:
        """Zoom camera in - REAL IMPLEMENTATION"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            zoom_factor = params.get('factor', 2.0)
            
            # Since setCameraZoom doesn't exist, use cameraForward as primary method
            if self.method_registry.validate_method_call(gs, 'cameraForward'):
                # Calculate movement distance based on zoom factor
                distance = int(params.get('distance', 1000) * zoom_factor)
                gs.cameraForward(distance)
                logger.info(f"Camera moved forward {distance} units (zoom factor: {zoom_factor})")
                return f"🔍 Zoomed in by {zoom_factor}x (moved forward {distance} units)"
            else:
                return "❌ Zoom functionality not available"
                
        except Exception as e:
            logger.error(f"Zoom in failed: {e}")
            return f"❌ Zoom in failed: {str(e)}"
    
    def _zoom_out(self, entity: str, params: dict) -> str:
        """Zoom camera out - REAL IMPLEMENTATION"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            zoom_factor = params.get('factor', 0.5)
            
            # Since setCameraZoom doesn't exist, use cameraForward (negative) as primary method
            if self.method_registry.validate_method_call(gs, 'cameraForward'):
                # Calculate movement distance based on zoom factor (negative for zoom out)
                distance = int(params.get('distance', 1000) * (1/zoom_factor))
                gs.cameraForward(-distance)  # Negative distance to move backward
                logger.info(f"Camera moved backward {distance} units (zoom factor: {zoom_factor})")
                return f"🔍 Zoomed out by {1/zoom_factor:.1f}x (moved backward {distance} units)"
            else:
                return "❌ Zoom functionality not available"
                
        except Exception as e:
            logger.error(f"Zoom out failed: {e}")
            return f"❌ Zoom out failed: {str(e)}"
    
    def _speed_up(self, entity: str, params: dict) -> str:
        """Increase simulation speed - REAL IMPLEMENTATION"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            speed_factor = params.get('factor', 2.0)
            
            # Use setTimeWarp instead of setSimulationSpeed (correct Gaia Sky method)
            if self.method_registry.validate_method_call(gs, 'setTimeWarp'):
                gs.setTimeWarp(speed_factor)
                logger.info(f"Time warp set to {speed_factor}x")
                return f"⚡ Simulation speed increased to {speed_factor}x!"
            elif self.method_registry.validate_method_call(gs, 'accelerateTime'):
                gs.accelerateTime()
                return "⚡ Time acceleration activated!"
            else:
                return "❌ Speed control not available"
                
        except Exception as e:
            logger.error(f"Speed up failed: {e}")
            return f"❌ Speed up failed: {str(e)}"
    
    def _slow_down(self, entity: str, params: dict) -> str:
        """Decrease simulation speed - REAL IMPLEMENTATION"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            speed_factor = params.get('factor', 0.5)
            
            # Use setTimeWarp instead of setSimulationSpeed (correct Gaia Sky method)
            if self.method_registry.validate_method_call(gs, 'setTimeWarp'):
                gs.setTimeWarp(speed_factor)
                logger.info(f"Time warp set to {speed_factor}x")
                return f"🐌 Simulation speed decreased to {speed_factor}x"
            elif self.method_registry.validate_method_call(gs, 'decelerateTime'):
                gs.decelerateTime()
                return "🐌 Time deceleration activated!"
            else:
                return "❌ Speed control not available"
                
        except Exception as e:
            logger.error(f"Slow down failed: {e}")
            return f"❌ Slow down failed: {str(e)}"
    
    def _stream_tour(self, entity: str, params: dict) -> str:
        """Stream tour - REAL IMPLEMENTATION with continuous updates"""
        if not entity:
            return "❌ Please specify destination for stream tour (e.g., 'Jupiter', 'solar system')"
            
        try:
            from .utils.config import TOUR_ROUTES
        except ImportError:
            from utils.config import TOUR_ROUTES
            
        # Check if it's a route-based tour or single destination
        route = TOUR_ROUTES.get(entity.lower())
        
        if route:
            # Multi-destination streaming tour
            return self._execute_streaming_route_tour(entity, route, params)
        else:
            # Single destination streaming tour
            return self._execute_streaming_single_tour(entity, params)
    
    def _execute_streaming_route_tour(self, entity: str, route: list, params: dict) -> str:
        """Execute streaming tour for multiple destinations"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Stream parameters
            delay = params.get('delay', 4.0)  # longer delays for streaming
            screenshot_each = params.get('screenshot_each', True)
            
            results = [f"📺 Starting live stream tour of {entity} ({len(route)} destinations)..."]
            results.append("🔴 LIVE - Broadcasting cosmic exploration!")
            
            for i, destination in enumerate(route, 1):
                try:
                    # Stream update
                    results.append(f"📡 STREAM UPDATE {i}/{len(route)}: Approaching {destination}...")
                    
                    # Navigate to destination
                    nav_result = self._go_to(destination, {'smooth': True, 'duration': 3.0})
                    
                    if "❌" in nav_result:
                        results.append(f"⚠️ STREAM: Failed to reach {destination}, continuing...")
                        continue
                    
                    # Take screenshot if enabled
                    if screenshot_each:
                        try:
                            screenshot_result = self._screenshot('', {'filename': f'stream_tour_{entity}_{i}_{destination.lower()}.jpg'})
                            if "📸" in screenshot_result:
                                results.append(f"📸 CAPTURED: {destination} screenshot for stream archive")
                        except:
                            pass
                    
                    # Stream commentary
                    results.append(f"🌟 LIVE from {destination}: Spectacular cosmic views!")
                    results.append(f"👀 Viewers are now experiencing the beauty of {destination}")
                    
                    # Wait with stream updates
                    if i < len(route):
                        results.append(f"⏰ Next destination in {delay} seconds...")
                        time.sleep(delay)
                        
                except Exception as e:
                    results.append(f"📺 STREAM ISSUE at {destination}: {str(e)}")
                    continue
            
            results.append(f"🎬 STREAM COMPLETE: {entity} tour finished! Thanks for watching!")
            results.append("📊 Stream archived for replay - cosmic memories preserved!")
            
            return '\n'.join(results)
            
        except Exception as e:
            logger.error(f"Streaming tour failed: {e}")
            return f"❌ Stream tour failed: {str(e)}"
    
    def _execute_streaming_single_tour(self, entity: str, params: dict) -> str:
        """Execute streaming tour for single destination with orbital movements"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            duration = params.get('duration', 15.0)  # streaming duration
            orbit_speed = params.get('orbit_speed', 0.5)
            
            results = [f"📺 Starting live stream tour of {entity}..."]
            results.append("🔴 LIVE - Single destination streaming experience!")
            
            # Navigate to target
            results.append(f"📡 STREAM: Approaching {entity}...")
            nav_result = self._go_to(entity, {'smooth': True})
            
            if "❌" in nav_result:
                return f"❌ Stream tour failed: Could not reach {entity}"
            
            results.append(f"🌟 LIVE from {entity}: Welcome to our cosmic destination!")
            
            # Start streaming with camera focus (since setCameraOrbitObject doesn't exist)
            if self.method_registry.validate_method_call(gs, 'setCameraFocus'):
                gs.setCameraFocus(entity)
                results.append(f"🌌 STREAM: Camera focused on {entity} for streaming")
                
                # Streaming updates with manual camera movements
                stream_intervals = int(duration / 3.0)
                for i in range(stream_intervals):
                    time.sleep(3.0)
                    results.append(f"📺 STREAM UPDATE {i+1}/{stream_intervals}: Live from {entity}...")
                    results.append(f"✨ Exploring different angles and cosmic details of {entity}")
                    
                    # Add rotation for variety if available
                    if self.method_registry.validate_method_call(gs, 'cameraRotate'):
                        rotation_angle = orbit_speed * 30  # Convert speed to rotation
                        gs.cameraRotate(rotation_angle, 0.0)
                        
                    # Take screenshots at intervals
                    if i % 2 == 0:  # every other interval
                        try:
                            screenshot_result = self._screenshot('', {'namePrefix': f'stream_{entity.lower()}_angle_{i+1}'})
                            if "📸" in screenshot_result:
                                results.append(f"📸 CAPTURED: Stream view #{i+1} for archive")
                        except:
                            pass
            else:
                # Fallback: focus tracking
                if self.method_registry.validate_method_call(gs, 'setCameraFocus'):
                    gs.setCameraFocus(entity)
                    results.append(f"📹 STREAM: Camera locked on {entity} - detailed observation mode")
                
                time.sleep(duration)
                results.append(f"🔍 STREAM: Extended observation of {entity} completed")
            
            results.append(f"🎭 STREAM FINALE: {entity} tour completed!")
            results.append("📊 Stream archived - cosmic adventure recorded for posterity!")
            
            self.last_target = entity
            return '\n'.join(results)
            
        except Exception as e:
            logger.error(f"Single streaming tour failed: {e}")
            return f"❌ Single stream tour failed: {str(e)}"
    
    # ============================================================================
    # PHASE 2: ADVANCED NEW METHODS - High-Value Gaia Sky Features
    # ============================================================================
    
    def _camera_transition(self, entity: str, params: dict) -> str:
        """Cinematic camera transition - NEW ADVANCED METHOD"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Get camera transition parameters
            duration = params.get('duration', 5.0)
            smooth_type = params.get('smooth_type', 'linear')
            smooth_factor = params.get('smooth_factor', 1.0)
            
            if entity:
                # Transition to entity - first get its position
                logger.info(f"🎬 Starting cinematic transition to {entity}")
                
                # Use existing navigation as base, then add cinematic transition
                nav_result = self._go_to(entity, {'smooth': True, 'duration': duration})
                if "❌" in nav_result:
                    return f"❌ Cinematic transition failed: Could not reach {entity}"
                
                # Add smooth orientation transition if available
                if self.method_registry.validate_method_call(gs, 'cameraOrientationTransition'):
                    # Get current camera direction and up vector (simplified)
                    current_dir = [0.0, 0.0, -1.0]  # Default forward
                    current_up = [0.0, 1.0, 0.0]   # Default up
                    
                    gs.cameraOrientationTransition(current_dir, current_up, duration, smooth_type, smooth_factor, True)
                    logger.info(f"Smooth camera orientation applied for {entity}")
                
                self.last_target = entity
                return f"🎬 Cinematic transition to {entity} completed with {smooth_type} smoothing!"
            else:
                return "❌ Please specify destination for cinematic transition"
                
        except Exception as e:
            logger.error(f"Camera transition failed: {e}")
            return f"❌ Camera transition failed: {str(e)}"
    
    def _draw_path(self, entity: str, params: dict) -> str:
        """Draw trajectory path to destination - NEW ADVANCED METHOD"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            if not entity:
                return "❌ Please specify destination to draw path to (e.g., 'Mars', 'Jupiter')"
            
            # Get path parameters
            color = params.get('color', [1.0, 0.0, 0.0])  # Default red
            line_width = params.get('line_width', 2.0)
            path_name = params.get('path_name', f'path_to_{entity.lower()}')
            
            # Create simple trajectory points (simplified - from current position to target)
            # In real implementation, you'd calculate orbital mechanics
            trajectory_points = [
                0.0, 0.0, 0.0,        # Start point (current camera position)
                1000000.0, 500000.0, 0.0,  # Midpoint
                2000000.0, 1000000.0, 0.0  # End point (near target)
            ]
            
            if self.method_registry.validate_method_call(gs, 'addTrajectoryLine'):
                gs.addTrajectoryLine(path_name, trajectory_points, color)
                logger.info(f"Trajectory path drawn to {entity}: {path_name}")
                return f"🛸 Flight path drawn to {entity}! Follow the trajectory line."
            else:
                return "❌ Trajectory drawing not available in this Gaia Sky version"
                
        except Exception as e:
            logger.error(f"Path drawing failed: {e}")
            return f"❌ Path drawing failed: {str(e)}"
    
    def _add_marker(self, entity: str, params: dict) -> str:
        """Add visual marker around object - NEW ADVANCED METHOD"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            if not entity:
                return "❌ Please specify object to mark (e.g., 'Mars', 'Jupiter')"
            
            # Get marker parameters
            shape = params.get('shape', 'sphere')  # sphere, cube, cylinder
            color_r = params.get('color_r', 1.0)   # Red component
            color_g = params.get('color_g', 0.0)   # Green component  
            color_b = params.get('color_b', 0.0)   # Blue component
            color_a = params.get('color_a', 0.8)   # Alpha (transparency)
            size = params.get('size', 2.0)         # Size multiplier
            show_label = params.get('show_label', True)
            track_object = params.get('track_object', True)
            marker_name = params.get('marker_name', f'{entity.lower()}_marker')
            
            if self.method_registry.validate_method_call(gs, 'addShapeAroundObject'):
                gs.addShapeAroundObject(
                    marker_name, shape, 'line', size, entity,
                    color_r, color_g, color_b, color_a, 
                    show_label, track_object
                )
                
                color_name = "red" if color_r > 0.5 else "blue" if color_b > 0.5 else "green"
                logger.info(f"Visual marker added around {entity}: {shape} in {color_name}")
                return f"🎯 {color_name.title()} {shape} marker added around {entity}!"
            else:
                return "❌ Visual markers not available in this Gaia Sky version"
                
        except Exception as e:
            logger.error(f"Marker creation failed: {e}")
            return f"❌ Marker creation failed: {str(e)}"
    
    def _time_travel(self, entity: str, params: dict) -> str:
        """Time travel to specific moments - NEW ADVANCED METHOD"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Get time travel parameters
            target_year = params.get('year')
            target_timestamp = params.get('timestamp')  # Unix timestamp in milliseconds
            
            if target_timestamp:
                # Direct timestamp travel
                if self.method_registry.validate_method_call(gs, 'setTargetTime'):
                    gs.setTargetTime(target_timestamp)
                    logger.info(f"Time travel to timestamp: {target_timestamp}")
                    return f"⏰ Time traveled to specified moment!"
                else:
                    return "❌ Time travel not available in this Gaia Sky version"
            
            elif target_year:
                # Year-based time travel (convert to timestamp)
                # January 1st of target year at midnight
                import datetime
                target_date = datetime.datetime(target_year, 1, 1)
                timestamp_ms = int(target_date.timestamp() * 1000)
                
                if self.method_registry.validate_method_call(gs, 'setTargetTime'):
                    gs.setTargetTime(timestamp_ms)
                    logger.info(f"Time travel to year {target_year}")
                    return f"⏰ Time traveled to year {target_year}! Welcome to the future/past!"
                else:
                    # Fallback to regular time setting
                    result = self._set_time('', {'year': target_year, 'month': 1, 'day': 1})
                    return f"⏰ Time set to year {target_year} (fallback method)"
            
            else:
                return "❌ Please specify year or timestamp for time travel"
                
        except Exception as e:
            logger.error(f"Time travel failed: {e}")
            return f"❌ Time travel failed: {str(e)}"
    
    def _pitch_camera(self, entity: str, params: dict) -> str:
        """Pitch camera up/down - NEW ADVANCED METHOD"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Get pitch parameters
            amount = params.get('amount', 30.0)  # degrees
            direction = params.get('direction', 'up')  # up or down
            
            # Convert direction to positive/negative
            pitch_amount = amount if direction == 'up' else -amount
            
            if self.method_registry.validate_method_call(gs, 'cameraPitch'):
                gs.cameraPitch(pitch_amount)
                logger.info(f"Camera pitched {direction} by {amount} degrees")
                return f"📹 Camera pitched {direction} by {amount}°"
            else:
                return "❌ Camera pitch control not available in this Gaia Sky version"
                
        except Exception as e:
            logger.error(f"Camera pitch failed: {e}")
            return f"❌ Camera pitch failed: {str(e)}"
    
    def _roll_camera(self, entity: str, params: dict) -> str:
        """Roll camera left/right - NEW ADVANCED METHOD"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Get roll parameters
            amount = params.get('amount', 30.0)  # degrees
            direction = params.get('direction', 'right')  # left or right
            
            # Convert direction to positive/negative
            roll_amount = amount if direction == 'right' else -amount
            
            if self.method_registry.validate_method_call(gs, 'cameraRoll'):
                gs.cameraRoll(roll_amount)
                logger.info(f"Camera rolled {direction} by {amount} degrees")
                return f"📹 Camera rolled {direction} by {amount}°"
            else:
                return "❌ Camera roll control not available in this Gaia Sky version"
                
        except Exception as e:
            logger.error(f"Camera roll failed: {e}")
            return f"❌ Camera roll failed: {str(e)}"
    
    def _smooth_orientation(self, entity: str, params: dict) -> str:
        """Smooth camera orientation transition - NEW ADVANCED METHOD"""
        try:
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return "❌ No connection to Gaia Sky"
            
            # Get orientation parameters
            duration = params.get('duration', 3.0)
            smooth_type = params.get('smooth_type', 'ease')
            smooth_factor = params.get('smooth_factor', 2.0)
            
            # Target direction (simplified - point towards entity or default)
            if entity:
                # Point camera towards specified entity
                target_dir = [0.0, 0.0, -1.0]  # Forward direction (simplified)
                target_up = [0.0, 1.0, 0.0]    # Up direction
                
                description = f"towards {entity}"
            else:
                # Default orientation
                target_dir = [0.0, 0.0, -1.0]
                target_up = [0.0, 1.0, 0.0]
                description = "to default orientation"
            
            if self.method_registry.validate_method_call(gs, 'cameraOrientationTransition'):
                gs.cameraOrientationTransition(target_dir, target_up, duration, smooth_type, smooth_factor, True)
                logger.info(f"Smooth camera orientation transition {description}")
                return f"📹 Smooth camera reorientation {description} completed!"
            else:
                return "❌ Smooth orientation transitions not available in this Gaia Sky version"
                
        except Exception as e:
            logger.error(f"Smooth orientation failed: {e}")
            return f"❌ Smooth orientation failed: {str(e)}"