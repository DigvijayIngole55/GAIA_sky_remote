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
    SPEECH_AVAILABLE = True
except ImportError:
    try:
        from speech_recognizer import UniversalSpeechRecognizer
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
  "action": "go_to|land_on|track|set_time|take_screenshot|explore|orbit|zoom_in|zoom_out|speed_up|slow_down|free_camera|stop_camera|back_to_space|tour|cinematic_journey|multi_step|stream_tour",
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
        
        # Map actions to methods
        self.action_map = {
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
            'slow_down': self._slow_down
        }
        
        logger.info("🚀 Astro Remote Controller initialized")
        
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
            
            # Use custom callback if provided, otherwise use default
            if custom_callback:
                command_handler = custom_callback
            else:
                def handle_speech_command(command: str):
                    """Handle commands from speech recognition"""
                    logger.info(f"Voice Command: '{command}'")
                    result = self.execute_command(command)
                    logger.info(f"Voice Result: {result}")
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
        command = self.llm.parse_command(user_input)
        if not command or not command.action:
            # return self._try_fallback_parsing(user_input)  # COMMENTED OUT - NO FALLBACK
            return f"❌ LLM failed to parse command: '{user_input}'"
        
        # Smart validation before execution
        should_execute, reason = self.should_execute_command(command.action, command.entity, current_state)
        
        if not should_execute:
            logger.info(f"🧠 SMART SKIP: {reason}")
            return f"🧠 Smart Agent: {reason}"
        
        logger.info(f"✅ EXECUTING: {command.action} {command.entity} - {reason}")
        
        # Execute command
        if command.action in self.action_map:
            result = self.action_map[command.action](command.entity, command.parameters or {})
            
            # Update last target for navigation commands
            if command.action in ['go_to', 'land_on', 'explore'] and command.entity:
                self.last_target = command.entity
                
            return result
        else:
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
                    self.last_target = entity
                    return f"✈️ Successfully navigated to {entity} (smooth)!"
                except Exception as e:
                    logger.warning(f"goToObjectSmooth failed: {e}, trying fallback...")
                
                # Fallback to basic goToObject
                try:
                    gs.goToObject(entity)
                    logger.info(f"Navigation to {entity} initiated (basic)")
                    self.last_target = entity
                    return f"✈️ Successfully navigated to {entity}!"
                except Exception as e:
                    logger.warning(f"goToObject failed: {e}")
            else:
                # Try instant navigation
                try:
                    gs.goToObjectInstant(entity)
                    logger.info(f"Instant navigation to {entity} completed")
                    self.last_target = entity
                    return f"✈️ Instantly navigated to {entity}!"
                except Exception as e:
                    logger.warning(f"goToObjectInstant failed: {e}, trying fallback...")
                
                # Fallback to basic goToObject
                try:
                    gs.goToObject(entity)
                    logger.info(f"Navigation to {entity} initiated (fallback)")
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
            
            # Wait for landing to complete
            time.sleep(2.0)  # Give time for landing animation
            
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
            
            # First navigate to the object
            if self.method_registry.validate_method_call(gs, 'goToObjectSmooth'):
                gs.goToObjectSmooth(entity)
                if self.method_registry.validate_method_call(gs, 'waitFocus'):
                    gs.waitFocus()
            
            # Set camera focus for exploration
            if self.method_registry.validate_method_call(gs, 'setCameraFocus'):
                gs.setCameraFocus(entity)
            
            # Optional: Add cinematic camera movement if available
            if hasattr(gs, 'cameraTransition') and self.method_registry.validate_method_call(gs, 'cameraTransition'):
                gs.cameraTransition(entity)
            
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
            quality = params.get('quality', 95)
            
            # Configure screenshot settings if available
            if self.method_registry.validate_method_call(gs, 'configureScreenshots'):
                gs.configureScreenshots(width, height, quality)
                logger.info(f"Screenshot configured: {width}x{height} at {quality}% quality")
            
            # Take the screenshot
            if self.method_registry.validate_method_call(gs, 'takeScreenshot'):
                gs.takeScreenshot()
                logger.info("Screenshot captured")
                
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
            
            # Set simulation time
            if self.method_registry.validate_method_call(gs, 'setSimulationTime'):
                gs.setSimulationTime(year, month, day, hour, minute, second)
                logger.info(f"Time set to {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")
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
                
                # Optional: Add smooth camera movement around the object
                if self.method_registry.validate_method_call(gs, 'setCameraOrbitObject'):
                    gs.setCameraOrbitObject(entity, 5.0, 0.3)  # slow orbit
                    results.append(f"🌌 Gentle orbital motion activated for cinematic effect")
            
            # Phase 4: Optional visual enhancements
            visual_effects = params.get('effects', True)
            if visual_effects:
                # Adjust time scale for dramatic effect if available
                if self.method_registry.validate_method_call(gs, 'setSimulationSpeed'):
                    try:
                        gs.setSimulationSpeed(0.2)  # slow motion effect
                        results.append("⏰ Time slowed for dramatic cinematic effect")
                        
                        # Reset to normal after a few seconds
                        time.sleep(3.0)
                        gs.setSimulationSpeed(1.0)
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
            
            # Set orbital camera mode if available
            if self.method_registry.validate_method_call(gs, 'setCameraOrbitObject'):
                gs.setCameraOrbitObject(entity, distance, speed)
                logger.info(f"Orbital camera set for {entity} (distance={distance}, speed={speed})")
                return f"🌌 Now orbiting {entity} at distance {distance}x with speed {speed}x!"
            elif self.method_registry.validate_method_call(gs, 'setCameraFocus'):
                # Fallback: just focus and track
                gs.setCameraFocus(entity)
                return f"🌌 Tracking {entity} (orbit mode not available, using focus tracking)"
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
            
            if self.method_registry.validate_method_call(gs, 'setCameraZoom'):
                current_zoom = getattr(gs, 'getCameraZoom', lambda: 1.0)()
                new_zoom = current_zoom * zoom_factor
                gs.setCameraZoom(new_zoom)
                logger.info(f"Camera zoomed in by factor {zoom_factor} (new zoom: {new_zoom})")
                return f"🔍 Zoomed in by {zoom_factor}x (total zoom: {new_zoom:.1f}x)"
            elif self.method_registry.validate_method_call(gs, 'cameraForward'):
                # Fallback: move camera forward
                distance = params.get('distance', 1000)
                gs.cameraForward(distance)
                return f"🔍 Moved camera forward {distance} units"
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
            
            if self.method_registry.validate_method_call(gs, 'setCameraZoom'):
                current_zoom = getattr(gs, 'getCameraZoom', lambda: 1.0)()
                new_zoom = current_zoom * zoom_factor
                gs.setCameraZoom(new_zoom)
                logger.info(f"Camera zoomed out by factor {1/zoom_factor} (new zoom: {new_zoom})")
                return f"🔍 Zoomed out by {1/zoom_factor:.1f}x (total zoom: {new_zoom:.1f}x)"
            elif self.method_registry.validate_method_call(gs, 'cameraBackward'):
                # Fallback: move camera backward
                distance = params.get('distance', 1000)
                gs.cameraBackward(distance)
                return f"🔍 Moved camera backward {distance} units"
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
            
            if self.method_registry.validate_method_call(gs, 'setSimulationSpeed'):
                # Get current speed if possible
                try:
                    current_speed = getattr(gs, 'getSimulationSpeed', lambda: 1.0)()
                    new_speed = current_speed * speed_factor
                    gs.setSimulationSpeed(new_speed)
                    logger.info(f"Simulation speed increased by {speed_factor}x (new speed: {new_speed})")
                    return f"⚡ Simulation speed increased to {new_speed:.1f}x!"
                except:
                    # Fallback: just set the factor directly
                    gs.setSimulationSpeed(speed_factor)
                    return f"⚡ Simulation speed set to {speed_factor}x!"
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
            
            if self.method_registry.validate_method_call(gs, 'setSimulationSpeed'):
                # Get current speed if possible
                try:
                    current_speed = getattr(gs, 'getSimulationSpeed', lambda: 1.0)()
                    new_speed = current_speed * speed_factor
                    gs.setSimulationSpeed(new_speed)
                    logger.info(f"Simulation speed decreased by {1/speed_factor}x (new speed: {new_speed})")
                    return f"🐌 Simulation speed decreased to {new_speed:.1f}x"
                except:
                    # Fallback: just set the factor directly
                    gs.setSimulationSpeed(speed_factor)
                    return f"🐌 Simulation speed set to {speed_factor}x"
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
            
            # Start orbital streaming if available
            if self.method_registry.validate_method_call(gs, 'setCameraOrbitObject'):
                gs.setCameraOrbitObject(entity, 8.0, orbit_speed)
                results.append(f"🌌 STREAM: Orbital camera activated - 360° views of {entity}")
                
                # Streaming updates during orbit
                stream_intervals = int(duration / 3.0)
                for i in range(stream_intervals):
                    time.sleep(3.0)
                    results.append(f"📺 STREAM UPDATE {i+1}/{stream_intervals}: Still orbiting {entity}...")
                    results.append(f"✨ Discovering new angles and cosmic details of {entity}")
                    
                    # Take screenshots at intervals
                    if i % 2 == 0:  # every other interval
                        try:
                            screenshot_result = self._screenshot('', {'filename': f'stream_{entity.lower()}_angle_{i+1}.jpg'})
                            if "📸" in screenshot_result:
                                results.append(f"📸 CAPTURED: Orbital view #{i+1} for stream archive")
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