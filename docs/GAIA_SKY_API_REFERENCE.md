# Gaia Sky API Reference - Real Method Signatures

**Complete documentation of actual Gaia Sky API methods available through the Java gateway**

*Based on Gaia Sky version 3.6.8 discovered on 2025-06-15*

## Overview

This document contains the **real** Gaia Sky API methods that can be called through the Python Py4J gateway. All methods are verified to exist in the actual Gaia Sky interface.

**Total Methods Available**: 292  
**Connection**: Py4J JavaGateway on port 25333  
**Method Categories**: Navigation, Camera, Screenshot, Time, and Utility

## Essential Navigation Methods

### Basic Navigation
```python
# Navigate to celestial objects
gs.goToObject(objectName)                    # Smooth navigation to object
gs.goToObjectInstant(objectName)             # Instant navigation to object  
gs.goToObjectSmooth(objectName)              # Extra smooth navigation to object

# Set camera focus
gs.setCameraFocus(objectName)                # Focus camera on object
gs.setCameraFocusInstant(objectName)         # Instant focus on object
gs.setCameraFocusInstantAndGo(objectName)    # Focus and navigate to object

# Landing operations
gs.landOnObject(objectName)                  # Land on celestial object
gs.landAtObjectLocation(objectName, lat, lon) # Land at specific coordinates
```

### Object Information
```python
# Get object properties
gs.getObject(objectName)                     # Get object reference
gs.getObjectPosition(objectName)             # Get object position
gs.getObjectRadius(objectName)               # Get object radius
gs.getObjectVisibility(objectName)           # Check if object visible
gs.getClosestObjectToCamera()                # Find nearest object to camera

# Object manipulation
gs.setObjectPosition(objectName, x, y, z)    # Set object position
gs.setObjectVisibility(objectName, visible)  # Show/hide object
gs.setObjectSizeScaling(objectName, scale)   # Scale object size
```

## Camera Control Methods

### Camera Position & Orientation
```python
# Get camera state
gs.getCameraPosition()                       # Get current camera position
gs.getCameraDirection()                      # Get camera direction vector
gs.getCameraUp()                            # Get camera up vector
gs.getCameraSpeed()                         # Get camera movement speed
gs.getCameraOrientationQuaternion()         # Get camera orientation

# Set camera properties
gs.setCameraPosition(x, y, z)               # Set camera position
gs.setCameraDirection(x, y, z)              # Set camera direction
gs.setCameraUp(x, y, z)                     # Set camera up vector
gs.setCameraSpeed(speed)                    # Set camera movement speed
gs.setCameraOrientationQuaternion(x, y, z, w) # Set camera orientation
```

### Camera Movement
```python
# Camera transitions
gs.cameraTransition(x, y, z, seconds)       # Smooth transition to position
gs.cameraTransitionKm(x, y, z, seconds)     # Transition with km coordinates
gs.cameraOrientationTransition(x, y, z, w, seconds) # Orientation transition

# Camera rotation
gs.cameraRotate(x, y, z, angle)             # Rotate camera around axis
gs.cameraTurn(angle, seconds)                # Turn camera by angle
gs.cameraYaw(angle, seconds)                 # Yaw camera rotation
gs.cameraPitch(angle, seconds)               # Pitch camera rotation
gs.cameraRoll(angle, seconds)                # Roll camera rotation

# Camera control
gs.cameraStop()                             # Stop camera movement
gs.cameraCenter()                           # Center camera
gs.cameraForward()                          # Move camera forward
```

### Camera Modes
```python
# Camera states
gs.setCameraFree()                           # Free camera mode
gs.setCameraLock()                          # Lock camera
gs.setCinematicCamera(enable)               # Cinematic camera mode
gs.setOrthosphereViewMode(enable)           # Orthosphere view mode

# Camera tracking
gs.setCameraTrackingObject(objectName)      # Track object with camera
gs.removeCameraTrackingObject()             # Stop tracking object
```

## Screenshot & Recording Methods

### Screenshots
```python
# Take screenshots
gs.takeScreenshot()                          # Take screenshot with default settings
gs.saveScreenshot(filename)                  # Save screenshot with custom filename
gs.configureScreenshots(width, height, quality) # Configure screenshot settings
gs.getDefaultScreenshotsDir()               # Get default screenshot directory
gs.setScreenshotsMode(mode)                 # Set screenshot mode
```

### Camera Recording
```python
# Camera path recording
gs.startRecordingCameraPath(filename)       # Start recording camera path
gs.stopRecordingCameraPath()                # Stop recording camera path
gs.runCameraPath(filename)                  # Run recorded camera path
gs.playCameraPath(filename)                 # Play camera path
gs.runCameraRecording(filename)             # Run camera recording
gs.setCameraRecorderFps(fps)                # Set recording FPS
```

## Time Control Methods

### Time Simulation
```python
# Time control
gs.setSimulationTime(year, month, day, hour, minute, second) # Set simulation time
gs.getSimulationTime()                      # Get current simulation time
gs.getSimulationTimeArr()                   # Get simulation time as array
gs.setSimulationPace(pace)                  # Set time acceleration
gs.setTimeWarp(factor)                      # Set time warp factor

# Time frames
gs.activateRealTimeFrame()                  # Use real-time frame
gs.activateSimulationTimeFrame()            # Use simulation time frame
gs.isSimulationTimeOn()                     # Check if simulation time active

# Time control
gs.startSimulationTime()                    # Start time simulation
gs.stopSimulationTime()                     # Stop time simulation
gs.setTargetTime(year, month, day, hour, minute, second) # Set target time
gs.unsetTargetTime()                        # Clear target time
gs.timeTransition(seconds)                  # Transition time smoothly
```

## Utility Methods

### GUI Control
```python
# GUI management
gs.enableGui()                              # Enable GUI
gs.disableGui()                             # Disable GUI
gs.enableInput()                            # Enable input
gs.disableInput()                           # Disable input

# GUI components
gs.expandGuiComponent(componentName)        # Expand GUI component
gs.collapseGuiComponent(componentName)      # Collapse GUI component
gs.expandUIPane(paneName)                   # Expand UI pane
gs.collapseUIPane(paneName)                 # Collapse UI pane
```

### Messages & Notifications
```python
# Display messages
gs.displayPopupNotification(message)        # Show popup notification
gs.displayMessageObject(message, x, y, z)   # Display 3D message
gs.displayTextObject(text, x, y, z)         # Display 3D text
gs.displayImageObject(imagePath, x, y, z)   # Display 3D image

# Clear messages
gs.clearAllMessages()                       # Clear all messages
gs.clearHeadlineMessage()                   # Clear headline message
gs.clearSubheadMessage()                    # Clear subhead message
```

### System Information
```python
# System info
gs.getBuildString()                         # Get Gaia Sky build info
gs.getAssetsLocation()                      # Get assets directory
gs.getDataDir()                             # Get data directory
gs.getConfigDir()                           # Get config directory
gs.getLocalDataDir()                        # Get local data directory

# Scene control
gs.forceUpdateScene()                       # Force scene update
gs.parkCameraRunnable()                     # Park camera runnable
```

## Coordinate System Methods

### Coordinate Conversions
```python
# Coordinate transformations
gs.equatorialToEcliptic(x, y, z)            # Equatorial to ecliptic coordinates
gs.eclipticToEquatorial(x, y, z)            # Ecliptic to equatorial coordinates
gs.galacticToEquatorial(x, y, z)            # Galactic to equatorial coordinates
gs.equatorialToGalactic(x, y, z)            # Equatorial to galactic coordinates

# Internal coordinate conversions
gs.equatorialToInternalCartesian(x, y, z)   # Equatorial to internal coordinates
gs.eclipticToInternalCartesian(x, y, z)     # Ecliptic to internal coordinates
gs.galacticToInternalCartesian(x, y, z)     # Galactic to internal coordinates
gs.equatorialCartesianToInternalCartesian(x, y, z) # Cartesian conversion
```

## Usage Examples

### Complete Navigation Example
```python
from py4j.java_gateway import JavaGateway

# Connect to Gaia Sky
gateway = JavaGateway()
gs = gateway.entry_point

# Navigate to Mars
gs.goToObject("Mars")
gs.waitFocus()  # Wait for navigation to complete

# Land on Mars
gs.landOnObject("Mars")

# Take screenshot
gs.takeScreenshot()

# Set camera focus on Jupiter
gs.setCameraFocus("Jupiter")

# Start tracking Jupiter
gs.setCameraTrackingObject("Jupiter")

# Set time to specific date
gs.setSimulationTime(2025, 6, 15, 12, 0, 0)

# Close connection
gateway.close()
```

### Camera Control Example
```python
# Get current camera position
pos = gs.getCameraPosition()
print(f"Camera position: {pos}")

# Move camera smoothly
gs.cameraTransition(1000, 0, 0, 5.0)  # Move to position over 5 seconds

# Rotate camera
gs.cameraRotate(0, 1, 0, 45)  # Rotate 45 degrees around Y axis

# Free camera mode
gs.setCameraFree()

# Stop all camera movement
gs.cameraStop()
```

### Screenshot and Recording Example
```python
# Configure screenshot settings
gs.configureScreenshots(1920, 1080, 95)  # Width, height, quality

# Take screenshot
gs.takeScreenshot()

# Start recording camera path
gs.startRecordingCameraPath("mars_flyby.gsc")

# Perform navigation
gs.goToObject("Mars")
gs.waitFocus()
gs.landOnObject("Mars")

# Stop recording
gs.stopRecordingCameraPath()

# Play back the recorded path
gs.runCameraPath("mars_flyby.gsc")
```

## Method Categories Summary

| Category | Methods | Description |
|----------|---------|-------------|
| **Navigation** | 40 | Object navigation, focus, landing, positioning |
| **Camera** | 45 | Camera control, movement, orientation, modes |
| **Screenshot** | 5 | Image capture, recording, configuration |
| **Time** | 14 | Time simulation, control, transitions |
| **Utility** | 188 | GUI, messages, coordinates, system info |

## Notes

1. **Object Names**: Use exact object names as they appear in Gaia Sky (e.g., "Mars", "Jupiter", "Sun")
2. **Coordinates**: Most methods use internal Gaia Sky coordinate system
3. **Timing**: Methods like `waitFocus()` should be used after navigation commands
4. **Connection**: Ensure Gaia Sky is running with Python bridge enabled
5. **Error Handling**: Wrap calls in try-catch blocks for robust operation

## Integration with Your Project

To replace the mock implementations in your `src/remote_controller.py`, use these patterns:

```python
def _go_to(self, entity: str, params: dict) -> str:
    """Navigate to celestial object - REAL IMPLEMENTATION"""
    try:
        gs = self.connection_manager.get_gaia_sky_interface()
        if not gs:
            return "❌ No connection to Gaia Sky"
        
        # Use real API call
        gs.goToObject(entity)
        gs.waitFocus()  # Wait for navigation to complete
        
        return f"✈️ Successfully navigated to {entity}"
    except Exception as e:
        return f"❌ Navigation failed: {str(e)}"

def _screenshot(self, entity: str, params: dict) -> str:
    """Take screenshot - REAL IMPLEMENTATION"""
    try:
        gs = self.connection_manager.get_gaia_sky_interface()
        if not gs:
            return "❌ No connection to Gaia Sky"
        
        # Use real API call
        gs.takeScreenshot()
        
        return "📸 Screenshot captured successfully!"
    except Exception as e:
        return f"❌ Screenshot failed: {str(e)}"
```

This reference provides all the real Gaia Sky API methods you need to implement actual space navigation functionality!