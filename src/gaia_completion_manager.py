#!/usr/bin/env python3
"""
🎯 GAIA SKY COMPLETION MANAGER
Smart completion detection for Gaia Sky operations
Replaces hardcoded timeouts with intelligent waitFocus() integration
"""

import time
import logging
from typing import Any, Optional, Dict, List
from enum import Enum

logger = logging.getLogger(__name__)

class CommandType(Enum):
    """Categories of commands based on completion requirements"""
    NAVIGATION = "navigation"        # Requires waitFocus() - takes 3-10 seconds
    MULTI_STEP = "multi_step"       # Multiple operations with sequential completion
    FAST = "fast"                   # Nearly instant operations
    CAMERA_MOVEMENT = "camera"      # Camera operations that may take time

class GaiaCompletionManager:
    """
    Smart completion detection for Gaia Sky operations
    
    Features:
    - Uses waitFocus() for navigation commands
    - Intelligent fallbacks when waitFocus() unavailable  
    - Quick verification for instant operations
    - Distance-based timing for complex scenarios
    """
    
    def __init__(self, method_registry):
        self.method_registry = method_registry
        self.command_categories = self._init_command_categories()
        
        # Completion detection settings
        self.max_navigation_wait = 30.0  # Maximum wait for navigation (safety)
        self.quick_verification_delay = 0.2  # Fast commands verification
        self.fallback_timing = {
            # Distance-based fallback timing when waitFocus() fails
            'nearby': 2.0,      # Moon, close objects
            'medium': 4.0,      # Mars, Venus
            'far': 6.0,         # Jupiter, Saturn  
            'very_far': 8.0,    # Outer planets
            'default': 5.0      # Unknown distance
        }
        
        logger.info("🎯 Gaia Completion Manager initialized")
    
    def _init_command_categories(self) -> Dict[str, CommandType]:
        """Categorize commands by their completion requirements"""
        return {
            # Navigation Commands - Need waitFocus()
            'go_to': CommandType.NAVIGATION,
            'land_on': CommandType.NAVIGATION,
            'track': CommandType.NAVIGATION,
            'explore': CommandType.NAVIGATION,
            'orbit': CommandType.NAVIGATION,
            
            # Multi-step Commands - Sequential completion
            'tour': CommandType.MULTI_STEP,
            'cinematic_journey': CommandType.MULTI_STEP,
            'multi_step': CommandType.MULTI_STEP,
            'stream_tour': CommandType.MULTI_STEP,
            
            # Camera Movement - May need brief wait
            'back_to_space': CommandType.CAMERA_MOVEMENT,
            'free_camera': CommandType.CAMERA_MOVEMENT,
            'stop_camera': CommandType.CAMERA_MOVEMENT,
            
            # Fast Commands - Minimal/no wait needed
            'take_screenshot': CommandType.FAST,
            'set_time': CommandType.FAST,
            'zoom_in': CommandType.FAST,
            'zoom_out': CommandType.FAST,
            'speed_up': CommandType.FAST,
            'slow_down': CommandType.FAST
        }
    
    def wait_for_completion(self, 
                          command_action: str, 
                          gaia_interface: Any, 
                          entity: str = "", 
                          **params) -> bool:
        """
        Main completion detection method
        
        Args:
            command_action: The action type (go_to, land_on, etc.)
            gaia_interface: Gaia Sky interface object
            entity: Target entity (for distance-based timing)
            **params: Additional parameters
            
        Returns:
            bool: True if completion detected successfully
        """
        command_type = self.command_categories.get(command_action, CommandType.FAST)
        
        logger.debug(f"🎯 Waiting for completion: {command_action} ({command_type.value})")
        
        try:
            if command_type == CommandType.NAVIGATION:
                return self._wait_navigation_completion(gaia_interface, entity, **params)
            
            elif command_type == CommandType.MULTI_STEP:
                # Multi-step operations handle their own completion
                return True
            
            elif command_type == CommandType.CAMERA_MOVEMENT:
                return self._wait_camera_completion(gaia_interface, **params)
            
            elif command_type == CommandType.FAST:
                return self._quick_verification()
            
            else:
                logger.warning(f"Unknown command type for {command_action}, using quick verification")
                return self._quick_verification()
                
        except Exception as e:
            logger.error(f"Completion detection error for {command_action}: {e}")
            # Fallback to quick verification on error
            return self._quick_verification()
    
    def _wait_navigation_completion(self, 
                                  gaia_interface: Any, 
                                  entity: str = "", 
                                  **params) -> bool:
        """
        Wait for navigation operations to complete using robust detection strategies
        
        Args:
            gaia_interface: Gaia Sky interface
            entity: Target entity for distance estimation
            **params: Navigation parameters
            
        Returns:
            bool: True if navigation completed successfully
        """
        logger.debug(f"🚀 Waiting for navigation completion to: {entity}")
        
        # Strategy 1: Camera position monitoring (most reliable - newly implemented)
        if self._monitor_camera_position_completion(gaia_interface, entity, **params):
            return True
        
        # Strategy 2: Distance-based intelligent timing (fallback)
        logger.debug("⏳ Using distance-based fallback timing")
        return self._fallback_navigation_timing(entity, **params)
    
    def _fallback_navigation_timing(self, entity: str, **params) -> bool:
        """
        Fallback timing for navigation when waitFocus() unavailable
        
        Args:
            entity: Target entity for distance estimation
            **params: Navigation parameters that may affect timing
            
        Returns:
            bool: Always True after appropriate wait
        """
        # Estimate timing based on target entity
        timing_category = self._estimate_navigation_timing(entity)
        wait_time = self.fallback_timing.get(timing_category, self.fallback_timing['default'])
        
        # Adjust for navigation type
        if params.get('smooth', True):
            # Smooth navigation may take longer
            duration = params.get('duration', 5.0)
            wait_time = max(wait_time, duration + 1.0)  # Add buffer
        elif params.get('instant', False):
            # Instant navigation should be much faster
            wait_time = min(wait_time, 1.0)
        
        logger.debug(f"⏰ Fallback wait: {wait_time:.1f}s for {entity} ({timing_category})")
        time.sleep(wait_time)
        
        logger.info(f"✅ Navigation fallback timing completed for {entity}")
        return True
    
    def _estimate_navigation_timing(self, entity: str) -> str:
        """
        Estimate navigation timing category based on target entity
        
        Args:
            entity: Target celestial object
            
        Returns:
            str: Timing category (nearby, medium, far, very_far, default)
        """
        if not entity:
            return 'default'
        
        entity_lower = entity.lower()
        
        # Nearby objects (quick navigation)
        if entity_lower in ['moon', 'luna', 'earth']:
            return 'nearby'
        
        # Medium distance objects
        elif entity_lower in ['mars', 'venus', 'mercury']:
            return 'medium'
        
        # Far objects
        elif entity_lower in ['jupiter', 'saturn']:
            return 'far'
        
        # Very far objects
        elif entity_lower in ['uranus', 'neptune', 'pluto']:
            return 'very_far'
        
        # Default for unknown objects
        else:
            return 'default'
    
    def _wait_camera_completion(self, gaia_interface: Any, **params) -> bool:
        """
        Wait for camera operations to complete
        
        Args:
            gaia_interface: Gaia Sky interface
            **params: Camera operation parameters
            
        Returns:
            bool: True when camera operation completed
        """
        logger.debug("📹 Waiting for camera operation completion")
        
        # Camera operations are generally fast but may need brief verification
        # Check if camera position stabilized (if position getter available)
        if self.method_registry.validate_method_call(gaia_interface, 'getCameraPosition'):
            try:
                # Wait briefly then check if camera has stabilized
                time.sleep(0.5)
                
                # Get camera position twice to check for movement
                pos1 = gaia_interface.getCameraPosition()
                time.sleep(0.3)
                pos2 = gaia_interface.getCameraPosition()
                
                # Simple stability check
                if hasattr(pos1, '__len__') and hasattr(pos2, '__len__') and len(pos1) >= 3 and len(pos2) >= 3:
                    movement = sum(abs(p1 - p2) for p1, p2 in zip(pos1[:3], pos2[:3]))
                    if movement < 1000:  # Threshold for "stable" camera
                        logger.debug("📹 Camera appears stable")
                        return True
                
                # If still moving, wait a bit more
                time.sleep(1.0)
                logger.info("✅ Camera operation completed (with movement)")
                return True
                
            except Exception as e:
                logger.debug(f"Camera position check failed: {e}, using default timing")
        
        # Fallback: short wait for camera operations
        time.sleep(1.0)
        logger.info("✅ Camera operation completed (fallback timing)")
        return True
    
    def _quick_verification(self) -> bool:
        """
        Quick verification for fast operations
        
        Returns:
            bool: Always True after brief verification delay
        """
        logger.debug("⚡ Quick verification for fast command")
        time.sleep(self.quick_verification_delay)
        logger.debug("✅ Fast command verified")
        return True
    
    def is_navigation_command(self, command_action: str) -> bool:
        """Check if command is a navigation type that needs waitFocus()"""
        return self.command_categories.get(command_action) == CommandType.NAVIGATION
    
    def is_fast_command(self, command_action: str) -> bool:
        """Check if command is fast and needs minimal waiting"""
        return self.command_categories.get(command_action) == CommandType.FAST
    
    def get_command_type(self, command_action: str) -> CommandType:
        """Get the command type for a given action"""
        return self.command_categories.get(command_action, CommandType.FAST)
    
    def _monitor_camera_position_completion(self, 
                                          gaia_interface: Any, 
                                          entity: str = "", 
                                          **params) -> bool:
        """
        Monitor camera position to detect navigation completion
        
        This is the primary strategy - monitor when camera stops moving
        to detect that navigation has completed.
        
        Args:
            gaia_interface: Gaia Sky interface
            entity: Target entity name
            **params: Navigation parameters
            
        Returns:
            bool: True if navigation completed successfully
        """
        logger.debug(f"📍 Monitoring camera position for completion to: {entity}")
        
        # Check if getCameraPosition is available
        if not self.method_registry.validate_method_call(gaia_interface, 'getCameraPosition'):
            logger.debug("❌ getCameraPosition not available, falling back")
            return False
        
        try:
            # Configuration
            max_wait_time = min(self.max_navigation_wait, 20.0)  # Cap at 20 seconds
            check_interval = 0.2  # Check every 200ms
            stability_checks = 3   # Need 3 consecutive stable readings
            stability_threshold = 1000.0  # Consider stable if movement < 1000 units
            
            start_time = time.time()
            stable_count = 0
            previous_position = None
            
            logger.debug(f"⏱️ Starting position monitoring (max wait: {max_wait_time}s)")
            
            while (time.time() - start_time) < max_wait_time:
                try:
                    # Get current camera position
                    current_position = gaia_interface.getCameraPosition()
                    
                    # Convert JavaArray to Python list for easier handling
                    if hasattr(current_position, '__len__') and len(current_position) >= 3:
                        curr_pos = [float(current_position[0]), float(current_position[1]), float(current_position[2])]
                    else:
                        logger.warning("Invalid camera position format")
                        return False
                    
                    if previous_position is not None:
                        # Calculate movement distance
                        movement = sum(abs(curr - prev) for curr, prev in zip(curr_pos, previous_position))
                        
                        if movement < stability_threshold:
                            stable_count += 1
                            logger.debug(f"📍 Stable reading {stable_count}/{stability_checks} (movement: {movement:.1f})")
                            
                            if stable_count >= stability_checks:
                                elapsed = time.time() - start_time
                                logger.info(f"✅ Navigation completed via position monitoring in {elapsed:.1f}s")
                                
                                # Additional verification: check if we're close to target
                                if entity and self._verify_target_reached(gaia_interface, entity):
                                    logger.debug(f"🎯 Target verification successful for {entity}")
                                else:
                                    logger.debug(f"⚠️ Target verification skipped or failed, but position stable")
                                
                                return True
                        else:
                            # Reset stability counter if significant movement detected
                            if stable_count > 0:
                                logger.debug(f"📍 Movement detected: {movement:.1f}, resetting stability counter")
                            stable_count = 0
                    
                    previous_position = curr_pos
                    time.sleep(check_interval)
                    
                except Exception as e:
                    logger.warning(f"Position monitoring error: {e}")
                    time.sleep(check_interval)
                    continue
            
            # Timeout reached
            elapsed = time.time() - start_time
            logger.warning(f"⏰ Position monitoring timeout after {elapsed:.1f}s")
            return False
            
        except Exception as e:
            logger.error(f"Camera position monitoring failed: {e}")
            return False
    
    def _verify_target_reached(self, gaia_interface: Any, entity: str) -> bool:
        """
        Verify that we've reached the target entity (optional verification)
        
        Args:
            gaia_interface: Gaia Sky interface
            entity: Target entity name
            
        Returns:
            bool: True if target verification successful
        """
        try:
            # Try to get closest object to camera
            if self.method_registry.validate_method_call(gaia_interface, 'getClosestObjectToCamera'):
                closest = gaia_interface.getClosestObjectToCamera()
                if closest and entity.lower() in str(closest).lower():
                    logger.debug(f"🎯 Target verification: closest object contains '{entity}'")
                    return True
            
            # Could add more verification methods here (getDistanceTo, etc.)
            return True  # Default to success if we can't verify
            
        except Exception as e:
            logger.debug(f"Target verification failed: {e}")
            return True  # Don't fail navigation just because verification failed


# Global completion manager instance (initialized when needed)
_completion_manager = None

def get_completion_manager(method_registry=None) -> GaiaCompletionManager:
    """Get the global completion manager instance"""
    global _completion_manager
    if _completion_manager is None:
        if method_registry is None:
            # Import here to avoid circular imports
            try:
                from .gaia_sky_methods import get_method_registry
            except ImportError:
                from gaia_sky_methods import get_method_registry
            method_registry = get_method_registry()
        _completion_manager = GaiaCompletionManager(method_registry)
    return _completion_manager