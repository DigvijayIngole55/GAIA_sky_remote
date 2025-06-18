#!/usr/bin/env python3
"""
STANDARDIZED GAIA SKY METHODS REGISTRY
Fixed toolset of the top 50 most essential Gaia Sky API methods
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class GaiaSkyMethod:
    """Gaia Sky method definition"""
    name: str
    category: str
    description: str
    parameters: List[str]
    required: bool = True

class GaiaSkyMethodRegistry:
    """Registry of validated Gaia Sky methods"""
    
    def __init__(self):
        self.methods = self._init_methods()
        self.method_cache = {}  # Cache for method availability
        
    def _init_methods(self) -> Dict[str, GaiaSkyMethod]:
        """Initialize the standardized method registry"""
        methods = {}
        
        # NAVIGATION METHODS (12 methods)
        navigation_methods = [
            ("goToObject", "Navigate to celestial object", ["objectName"]),
            ("goToObjectInstant", "Instant navigation", ["objectName"]),
            ("goToObjectSmooth", "Smooth navigation", ["objectName"]),
            ("setCameraFocus", "Focus camera on object", ["objectName"]),
            ("setCameraFocusInstant", "Instant focus", ["objectName"]),
            ("setCameraFocusInstantAndGo", "Focus and navigate", ["objectName"]),
            ("landOnObject", "Land on celestial body", ["objectName"]),
            ("landAtObjectLocation", "Land at coordinates", ["objectName", "latitude", "longitude"]),
            ("waitFocus", "Wait for navigation completion", []),
            ("getClosestObjectToCamera", "Find nearest object", []),
            ("setObjectVisibility", "Show/hide objects", ["objectName", "visible"]),
            ("addShapeAroundObject", "Add visual markers", ["objectName", "shape"])
        ]
        
        for name, desc, params in navigation_methods:
            methods[name] = GaiaSkyMethod(name, "navigation", desc, params)
        
        # CAMERA CONTROL METHODS (15 methods)
        camera_methods = [
            ("cameraStop", "Stop all camera movement", []),
            ("setCameraFree", "Free camera mode", []),
            ("getCameraPosition", "Get camera coordinates", []),
            ("setCameraPosition", "Set camera position", ["x", "y", "z"]),
            ("cameraCenter", "Center camera", []),
            ("cameraForward", "Move camera forward", ["distance"]),
            ("cameraRotate", "Rotate camera", ["angle"]),
            ("cameraTurn", "Turn camera", ["angle"]),
            ("cameraYaw", "Camera yaw control", ["angle"]),
            ("cameraPitch", "Camera pitch control", ["angle"]),
            ("cameraRoll", "Camera roll control", ["angle"]),
            ("cameraTransition", "Smooth camera transition", ["target"]),
            ("cameraTransitionKm", "Distance-based transition", ["distance"]),
            ("cameraOrientationTransition", "Orientation change", ["orientation"]),
            ("cameraPositionTransition", "Position change", ["x", "y", "z"])
        ]
        
        for name, desc, params in camera_methods:
            methods[name] = GaiaSkyMethod(name, "camera", desc, params)
        
        # SCREENSHOT METHODS (5 methods)
        screenshot_methods = [
            ("takeScreenshot", "Capture screen", []),
            ("configureScreenshots", "Set quality/resolution", ["width", "height", "quality"]),
            ("saveScreenshot", "Save with filename", ["filename"]),
            ("configureFrameOutput", "Frame settings", ["settings"]),
            ("configureRenderOutput", "Render settings", ["settings"])
        ]
        
        for name, desc, params in screenshot_methods:
            methods[name] = GaiaSkyMethod(name, "screenshot", desc, params)
        
        # TIME CONTROL METHODS (6 methods)
        time_methods = [
            ("setSimulationTime", "Set date/time", ["year", "month", "day", "hour", "minute", "second"]),
            ("getSimulationTime", "Get current time", []),
            ("getSimulationTimeArr", "Get time array", []),
            ("setSimulationPace", "Set time speed", ["pace"]),
            ("activateRealTimeFrame", "Real-time mode", []),
            ("activateSimulationTimeFrame", "Simulation mode", [])
        ]
        
        for name, desc, params in time_methods:
            methods[name] = GaiaSkyMethod(name, "time", desc, params)
        
        # OBJECT INFORMATION METHODS (8 methods)
        object_methods = [
            ("getObject", "Get object reference", ["objectName"]),
            ("getObjectPosition", "Get coordinates", ["objectName"]),
            ("getObjectPredictedPosition", "Predicted location", ["objectName", "time"]),
            ("getObjectRadius", "Get size", ["objectName"]),
            ("getObjectScreenCoordinates", "Screen position", ["objectName"]),
            ("getObjectVisibility", "Check visibility", ["objectName"]),
            ("setObjectPosition", "Move objects", ["objectName", "x", "y", "z"]),
            ("setObjectSizeScaling", "Scale objects", ["objectName", "scale"])
        ]
        
        for name, desc, params in object_methods:
            methods[name] = GaiaSkyMethod(name, "object", desc, params)
        
        # UTILITY METHODS (4 methods)
        utility_methods = [
            ("enableInput", "Enable controls", []),
            ("disableInput", "Disable controls", []),
            ("enableGui", "Show interface", []),
            ("disableGui", "Hide interface", [])
        ]
        
        for name, desc, params in utility_methods:
            methods[name] = GaiaSkyMethod(name, "utility", desc, params)
        
        return methods
    
    def get_method(self, name: str) -> Optional[GaiaSkyMethod]:
        """Get method definition by name"""
        return self.methods.get(name)
    
    def method_exists(self, name: str) -> bool:
        """Check if method exists in registry"""
        return name in self.methods
    
    def get_methods_by_category(self, category: str) -> List[GaiaSkyMethod]:
        """Get all methods in a category"""
        return [method for method in self.methods.values() if method.category == category]
    
    def validate_method_call(self, gs_interface: Any, method_name: str) -> bool:
        """Validate that method exists on Gaia Sky interface"""
        if method_name in self.method_cache:
            return self.method_cache[method_name]
        
        try:
            # Check if method exists on the interface
            exists = hasattr(gs_interface, method_name)
            self.method_cache[method_name] = exists
            
            if not exists:
                logger.warning(f"Method '{method_name}' not available on Gaia Sky interface")
            
            return exists
        except Exception as e:
            logger.error(f"Error validating method '{method_name}': {e}")
            self.method_cache[method_name] = False
            return False
    
    def get_all_method_names(self) -> List[str]:
        """Get list of all method names"""
        return list(self.methods.keys())
    
    def get_navigation_methods(self) -> List[str]:
        """Get essential navigation method names"""
        return [
            "goToObject", "goToObjectSmooth", "goToObjectInstant",
            "setCameraFocus", "setCameraFocusInstant", "landOnObject",
            "landAtObjectLocation", "waitFocus"
        ]
    
    def get_camera_methods(self) -> List[str]:
        """Get essential camera control method names"""
        return [
            "cameraStop", "setCameraFree", "getCameraPosition", 
            "setCameraPosition", "cameraCenter"
        ]
    
    def get_screenshot_methods(self) -> List[str]:
        """Get screenshot method names"""
        return ["takeScreenshot", "configureScreenshots", "saveScreenshot"]

# Global registry instance
method_registry = GaiaSkyMethodRegistry()

def get_method_registry() -> GaiaSkyMethodRegistry:
    """Get the global method registry instance"""
    return method_registry