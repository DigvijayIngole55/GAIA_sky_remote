# Gaia Sky API - Quick Reference Guide

**Essential methods for immediate use in your remote controller**

## Most Important Methods

### 🚀 Navigation (Essential)
```python
gs.goToObject("Mars")              # Navigate to object
gs.goToObjectInstant("Jupiter")    # Instant navigation  
gs.goToObjectSmooth("Saturn")      # Extra smooth navigation
gs.setCameraFocus("Venus")         # Focus camera on object
gs.waitFocus()                     # Wait for navigation to complete
```

### 🛬 Landing
```python
gs.landOnObject("Moon")                      # Land on object
gs.landAtObjectLocation("Mars", 45.0, -90.0) # Land at coordinates
```

### 📸 Screenshots
```python
gs.takeScreenshot()                          # Take screenshot
gs.configureScreenshots(1920, 1080, 95)     # Configure quality
gs.saveScreenshot("my_image.png")           # Save with filename
```

### 📹 Camera Control
```python
gs.getCameraPosition()             # Get camera position [x, y, z]
gs.setCameraPosition(x, y, z)      # Set camera position
gs.cameraStop()                    # Stop all camera movement
gs.setCameraFree()                 # Free camera mode
gs.setCameraTrackingObject("Mars") # Track object with camera
```

### ⏰ Time Control
```python
gs.setSimulationTime(2025, 6, 15, 12, 0, 0)  # Set date/time
gs.setSimulationPace(100)                     # Set time speed (100x)
gs.getSimulationTime()                        # Get current time
```

## Quick Implementation Pattern

Replace your mock methods with this pattern:

```python
def _go_to(self, entity: str, params: dict) -> str:
    try:
        gs = self.connection_manager.get_gaia_sky_interface()
        if not gs:
            return "❌ No connection to Gaia Sky"
        
        # REAL API CALL
        gs.goToObject(entity)
        gs.waitFocus()
        
        return f"✈️ Successfully navigated to {entity}"
    except Exception as e:
        return f"❌ Navigation failed: {str(e)}"
```

## Object Names (Case Sensitive)
- **Planets**: Mars, Jupiter, Saturn, Venus, Mercury, Neptune, Uranus, Pluto
- **Moons**: Moon, Europa, Io, Ganymede, Callisto, Titan, Enceladus
- **Stars**: Sun, "Alpha Centauri", Sirius, Betelgeuse, Vega
- **Other**: Earth, ISS, Hubble

## Common Parameters

### Navigation Parameters
```python
# Smooth vs Instant
gs.goToObject("Mars")        # Default smooth
gs.goToObjectInstant("Mars") # Instant teleport
gs.goToObjectSmooth("Mars")  # Extra smooth

# With focus
gs.setCameraFocusInstantAndGo("Jupiter") # Focus + Navigate
```

### Screenshot Parameters
```python
# Configure before taking
gs.configureScreenshots(width, height, quality)
gs.takeScreenshot()

# Common configurations
gs.configureScreenshots(1920, 1080, 95)  # Full HD, high quality
gs.configureScreenshots(3840, 2160, 100) # 4K, max quality
```

### Camera Parameters
```python
# Position (x, y, z coordinates)
gs.setCameraPosition(1000.0, 0.0, 0.0)

# Transitions with timing
gs.cameraTransition(x, y, z, seconds)
gs.cameraOrientationTransition(x, y, z, w, seconds)
```

## Error Handling Pattern

Always wrap API calls:

```python
try:
    gs = self.connection_manager.get_gaia_sky_interface()
    if not gs:
        return "❌ No connection to Gaia Sky"
    
    # Your API call here
    gs.someMethod(parameters)
    
    return "✅ Success message"
    
except Exception as e:
    logger.error(f"Operation failed: {e}")
    return f"❌ Operation failed: {str(e)}"
```

## Testing Connection

```python
# Test if connection works
try:
    gs = gateway.entry_point
    # Simple test call
    pos = gs.getCameraPosition()
    print(f"✅ Connected! Camera at: {pos}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

## Integration Steps

1. **Replace mock methods** in `src/remote_controller.py`
2. **Add error handling** for all API calls  
3. **Test each method** individually
4. **Add logging** for debugging
5. **Handle edge cases** (no connection, invalid objects)

## Ready-to-Use Replacements

Copy these into your `remote_controller.py`:

```python
def _go_to(self, entity: str, params: dict) -> str:
    if not entity:
        return "❌ Please specify destination"
    try:
        gs = self.connection_manager.get_gaia_sky_interface()
        if not gs:
            return "❌ No connection to Gaia Sky"
        gs.goToObject(entity)
        gs.waitFocus()
        return f"✈️ Navigated to {entity}"
    except Exception as e:
        return f"❌ Navigation failed: {str(e)}"

def _screenshot(self, entity: str, params: dict) -> str:
    try:
        gs = self.connection_manager.get_gaia_sky_interface()
        if not gs:
            return "❌ No connection to Gaia Sky"
        gs.takeScreenshot()
        return "📸 Screenshot captured!"
    except Exception as e:
        return f"❌ Screenshot failed: {str(e)}"

def _land_on(self, entity: str, params: dict) -> str:
    if not entity:
        return "❌ Please specify landing target"
    try:
        gs = self.connection_manager.get_gaia_sky_interface()
        if not gs:
            return "❌ No connection to Gaia Sky"
        gs.landOnObject(entity)
        return f"🛬 Landed on {entity}"
    except Exception as e:
        return f"❌ Landing failed: {str(e)}"
```

## Next Steps

1. **Review the full API reference**: `GAIA_SKY_API_REFERENCE.md`
2. **Study implementation examples**: `REAL_API_IMPLEMENTATION_EXAMPLES.py`  
3. **Test each method** with your Gaia Sky installation
4. **Replace mock implementations** one by one
5. **Add robust error handling** for production use

**You now have access to 292 real Gaia Sky API methods!** 🚀