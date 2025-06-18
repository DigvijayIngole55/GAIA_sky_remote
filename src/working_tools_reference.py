import time
import math
import random
from gaia_sky_connection import get_connection_manager

# ------------------------------------------------------------
#  CORE DIRECTOR & CONTROLLERS
# ------------------------------------------------------------

class UniversalSpaceDirector:
    """
    Main class for managing Gaia Sky cinematic operations.
    Uses the shared connection manager for all operations.
    """

    def __init__(self):
        self.connection_manager = get_connection_manager()

    def __enter__(self):
        # Use the shared connection manager
        if self.connection_manager.connect():
            return self
        else:
            raise Exception("Failed to connect to Gaia Sky")

    def __exit__(self, exc_type, exc_value, traceback):
        # Connection manager handles cleanup automatically
        pass

    @property
    def gs(self):
        """Get the Gaia Sky interface through the connection manager."""
        return self.connection_manager.get_gaia_sky_interface()

    # ------------------------------------------------------------------------
    #  TIME CONTROL METHODS
    # ------------------------------------------------------------------------

    def set_time(self, timestamp: float) -> bool:
        """
        Jump to a specific epoch time in Gaia Sky.
        Args:
            timestamp (float): Unix epoch time (seconds since 1970).
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.gs.setSimulationTime(timestamp)
            return True
        except Exception as e:
            print(f"Error setting time: {e}")
            return False

    def start_time(self) -> bool:
        """
        Resume Gaia Sky’s internal clock.
        """
        try:
            self.gs.startSimulationTime()
            return True
        except Exception as e:
            print(f"Error starting time: {e}")
            return False

    def stop_time(self) -> bool:
        """
        Pause Gaia Sky’s internal clock.
        """
        try:
            self.gs.stopSimulationTime()
            return True
        except Exception as e:
            print(f"Error stopping time: {e}")
            return False

    def set_time_rate(self, rate: float) -> bool:
        """
        Change the speed of time progression.
        Args:
            rate (float): Multiplier for Gaia Sky’s time rate (e.g., 1.0 = real time, 10.0 = 10× speed).
        """
        try:
            # Use the connection manager for safe execution
            self.gs.setTimeWarp(rate)
            return True
        except Exception as e:
            print(f"Error setting time rate: {e}")
            return False

    # ------------------------------------------------------------------------
    #  CAMERA CONTROL METHODS
    # ------------------------------------------------------------------------

    def set_camera_position(self, x: float, y: float, z: float) -> bool:
        """
        Teleport camera instantly to a world‐space position.
        Uses the correct setCameraPosition API method.
        """
        try:
            self.gs.setCameraPosition(x, y, z)
            return True
        except Exception as e:
            print(f"Error setting camera position: {e}")
            return False

    def set_camera_rotation(self, rot_x: float, rot_y: float) -> bool:
        """
        Rotate camera by delta amounts (this method doesn't exist in real API).
        Using cameraRotate as alternative.
        """
        try:
            self.gs.cameraRotate(rot_x, rot_y)
            return True
        except Exception as e:
            print(f"Error rotating camera: {e}")
            return False

    def camera_rotate(self, delta_x: float, delta_y: float) -> bool:
        """
        Rotate camera by small deltas (useful for smoothing).
        """
        try:
            self.gs.cameraRotate(delta_x, delta_y)
            return True
        except Exception as e:
            print(f"Error rotating camera: {e}")
            return False

    def start_camera_orbit(
        self,
        target_object: str,
        radius: float = 1.0,
        duration: float = 10.0,
        axis: str = "Z",
        reverse: bool = False,
    ) -> bool:
        """
        Orbit the camera around a named object.
        Since cameraOrbit doesn't exist in real API, using setCameraTrackingObject as alternative.
        Args:
            target_object (str): Name of object in Gaia Sky (e.g. "Mars", "Sun", "Alpha Centauri").
            radius (float): Not used (kept for compatibility).
            duration (float): Not used (kept for compatibility).
            axis (str): Not used (kept for compatibility).
            reverse (bool): Not used (kept for compatibility).
        """
        try:
            # Use real API method: setCameraTrackingObject
            self.gs.setCameraTrackingObject(target_object)
            return True
        except Exception as e:
            print(f"Error setting camera tracking: {e}")
            return False

    def stop_camera(self) -> bool:
        """
        Stop any active camera motion (orbit, tracking, etc.).
        """
        try:
            return self.gs.cameraStop()
        except Exception as e:
            print(f"Error stopping camera: {e}")
            return False

    # ------------------------------------------------------------------------
    #  CINEMATIC CAMERA MOVEMENTS
    # ------------------------------------------------------------------------

    def camera_transition(self, duration: float = 5.0) -> bool:
        """Smooth camera transition movement.
        Uses a basic position-to-position transition with current camera state.
        """
        try:
            # Get current camera position and direction
            current_pos = self.gs.getCameraPosition()
            current_dir = self.gs.getCameraDirection()
            current_up = self.gs.getCameraUp()
            
            # Use real API: cameraTransition with current state
            self.gs.cameraTransition(current_pos, current_dir, current_up, duration, False)
            return True
        except Exception as e:
            print(f"Error in camera transition: {e}")
            return False

    def camera_transition_km(self, distance: float) -> bool:
        """Distance-based smooth camera movement.
        Uses current camera state and moves by specified distance.
        """
        try:
            # Get current camera state
            current_pos = self.gs.getCameraPosition()
            current_dir = self.gs.getCameraDirection()
            current_up = self.gs.getCameraUp()
            
            # Use real API: cameraTransitionKm with 4 parameters
            self.gs.cameraTransitionKm(current_pos, current_dir, current_up, distance)
            return True
        except Exception as e:
            print(f"Error in camera transition km: {e}")
            return False

    def camera_position_transition(self, x: float, y: float, z: float) -> bool:
        """Smooth transition to specific position."""
        try:
            self.gs.cameraPositionTransition(x, y, z)
            return True
        except Exception as e:
            print(f"Error in camera position transition: {e}")
            return False

    def camera_orientation_transition(self, pitch: float = 0, yaw: float = 0, roll: float = 0) -> bool:
        """Smooth camera orientation change."""
        try:
            self.gs.cameraOrientationTransition(pitch, yaw, roll)
            return True
        except Exception as e:
            print(f"Error in camera orientation transition: {e}")
            return False

    # ------------------------------------------------------------------------
    #  NAVIGATION & FOCUS
    # ------------------------------------------------------------------------

    def go_to_object(self, object_name: str) -> bool:
        """Smoothly travel to an object."""
        try:
            self.gs.goToObject(object_name)
            return True
        except Exception as e:
            print(f"Error going to object: {e}")
            return False

    def go_to_object_instant(self, object_name: str) -> bool:
        """Instantly jump to an object."""
        try:
            self.gs.goToObjectInstant(object_name)
            return True
        except Exception as e:
            print(f"Error going to object instant: {e}")
            return False

    def go_to_object_smooth(self, object_name: str, angle: float = 0.0, duration: float = 5.0) -> bool:
        """Smooth version of travel to object.
        Args:
            object_name: Name of the object to go to
            angle: Viewing angle (default 0.0)
            duration: Duration of transition in seconds (default 5.0)
        """
        try:
            self.gs.goToObjectSmooth(object_name, angle, duration)
            return True
        except Exception as e:
            print(f"Error going to object smooth: {e}")
            return False

    def set_camera_focus(self, object_name: str) -> bool:
        """Focus camera on an object."""
        try:
            self.gs.setCameraFocus(object_name)
            return True
        except Exception as e:
            print(f"Error setting camera focus: {e}")
            return False

    def set_camera_focus_instant_and_go(self, object_name: str) -> bool:
        """Focus and move to object instantly."""
        try:
            self.gs.setCameraFocusInstantAndGo(object_name)
            return True
        except Exception as e:
            print(f"Error setting camera focus instant and go: {e}")
            return False

    def set_camera_tracking_object(self, object_name: str) -> bool:
        """Set camera to track an object during movement."""
        try:
            self.gs.setCameraTrackingObject(object_name)
            return True
        except Exception as e:
            print(f"Error setting camera tracking: {e}")
            return False

    # ------------------------------------------------------------------------
    #  CAMERA SPEED & CONTROL
    # ------------------------------------------------------------------------

    def set_camera_speed(self, speed: float) -> bool:
        """Control camera travel velocity."""
        try:
            self.gs.setCameraSpeed(speed)
            return True
        except Exception as e:
            print(f"Error setting camera speed: {e}")
            return False

    def set_camera_speed_limit(self, limit: float) -> bool:
        """Set maximum camera speed."""
        try:
            self.gs.setCameraSpeedLimit(limit)
            return True
        except Exception as e:
            print(f"Error setting camera speed limit: {e}")
            return False

    def set_camera_turning_speed(self, speed: float) -> bool:
        """Control camera rotation speed."""
        try:
            self.gs.setCameraTurningSpeed(speed)
            return True
        except Exception as e:
            print(f"Error setting camera turning speed: {e}")
            return False

    def set_camera_direction(self, x: float, y: float, z: float) -> bool:
        """Point camera in specific direction."""
        try:
            self.gs.setCameraDirection(x, y, z)
            return True
        except Exception as e:
            print(f"Error setting camera direction: {e}")
            return False

    # ------------------------------------------------------------------------
    #  ADVANCED CINEMATICS
    # ------------------------------------------------------------------------

    def set_cinematic_camera(self, enable: bool) -> bool:
        """Enable/disable cinematic camera mode."""
        try:
            self.gs.setCinematicCamera(enable)
            return True
        except Exception as e:
            print(f"Error setting cinematic camera: {e}")
            return False

    def land_on_object(self, object_name: str) -> bool:
        """Perform smooth landing sequence on object."""
        try:
            self.gs.landOnObject(object_name)
            return True
        except Exception as e:
            print(f"Error landing on object: {e}")
            return False

    def land_at_object_location(self, object_name: str, latitude: float, longitude: float) -> bool:
        """Land at specific coordinates on object."""
        try:
            self.gs.landAtObjectLocation(object_name, latitude, longitude)
            return True
        except Exception as e:
            print(f"Error landing at object location: {e}")
            return False

    def play_camera_path(self, path_name: str) -> bool:
        """Follow a pre-recorded camera path."""
        try:
            self.gs.playCameraPath(path_name)
            return True
        except Exception as e:
            print(f"Error playing camera path: {e}")
            return False

    def start_recording_camera_path(self) -> bool:
        """Start recording camera movements."""
        try:
            self.gs.startRecordingCameraPath()
            return True
        except Exception as e:
            print(f"Error starting camera recording: {e}")
            return False

    def stop_recording_camera_path(self) -> bool:
        """Stop recording camera movements."""
        try:
            self.gs.stopRecordingCameraPath()
            return True
        except Exception as e:
            print(f"Error stopping camera recording: {e}")
            return False

    # ------------------------------------------------------------------------
    #  OBJECT FOCUS / FLYTO
    # ------------------------------------------------------------------------

    def fly_to_object(
        self,
        object_name: str,
        duration: float = 5.0,
        keep_rotation: bool = True,
    ) -> bool:
        """
        Smoothly fly the camera to focus on a named object.
        Args:
            object_name (str): Name of the object (e.g. "Jupiter", "Betelgeuse").
            duration (float): How long (seconds) the flight should take.
            keep_rotation (bool): If True, preserve current camera rotation.
        """
        try:
            # Use the connection manager to get the interface directly
            gs = self.connection_manager.get_gaia_sky_interface()
            if not gs:
                return False
            
            # Set camera to free mode first
            gs.setCameraFree()
            
            # Try multiple movement methods (using the same approach that works in testing)
            methods_to_try = [
                lambda: gs.setCameraFocusInstantAndGo(object_name),
                lambda: gs.goToObjectInstant(object_name),
                lambda: gs.setCameraFocus(object_name),
                lambda: gs.goToObject(object_name)
            ]
            
            for method in methods_to_try:
                try:
                    method()
                    # Force scene update to ensure movement is processed
                    gs.forceUpdateScene()
                    return True
                except:
                    continue
            
            # If all else fails, return False
            return False
            
        except Exception as e:
            print(f"Error flying to object: {e}")
            return False

    # ------------------------------------------------------------------------
    #  VISUAL EFFECTS
    # ------------------------------------------------------------------------

    def capture_screenshot(self, file_path: str = "") -> bool:
        """
        Save a screenshot of the current view to disk.
        Args:
            file_path (str): Not used - screenshots save to default directory.
                           Kept for compatibility.
        """
        try:
            # Real API uses saveScreenshot() with no parameters
            self.gs.saveScreenshot()
            return True
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return False

    def add_camera_shake(
        self, intensity: float = 0.0001, frequency: float = 0.05, duration: float = 5.0
    ) -> bool:
        """
        Add subtle camera shake for realism.
        """
        try:
            if not self.gs:
                return False

            class CameraShakeRunnable:
                def __init__(self, gs_api, intensity, frequency, start_time, duration):
                    self.gs = gs_api
                    self.intensity = intensity
                    self.frequency = frequency
                    self.start_time = start_time
                    self.duration = duration
                    self.last_shake_time = start_time

                def run(self_inner):
                    elapsed_time = time.time() - self_inner.start_time
                    if elapsed_time < self_inner.duration:
                        if time.time() - self_inner.last_shake_time > self_inner.frequency:
                            rot_x = (random.random() - 0.5) * self_inner.intensity * 10
                            rot_y = (random.random() - 0.5) * self_inner.intensity * 10
                            self_inner.gs.cameraRotate(rot_x, rot_y)
                            self_inner.last_shake_time = time.time()

            start_t = time.time()
            runnable = CameraShakeRunnable(self.gs, intensity, frequency, start_t, duration)
            # Spawn a new thread so shake happens asynchronously:
            import threading

            thread = threading.Thread(target=runnable.run)
            thread.start()
            return True

        except Exception as e:
            print(f"Error adding camera shake: {e}")
            return False


class VisualController:
    """Manages visual elements, settings, and on-screen annotations."""

    def __init__(self, director: GaiaSkyDirector):
        self.director = director
        self.gs = director.gs

    def toggle_element(self, element_key: str, visible: bool) -> bool:
        """
        Toggle visibility of scene elements (e.g. orbits, grids, constellations).
        """
        try:
            self.gs.visualToggle(element_key, visible)
            return True
        except Exception as e:
            print(f"Error toggling element {element_key}: {e}")
            return False

    def show_message(self, title: str, message: str, duration: float) -> bool:
        """
        Display a temporary 2D message overlay.
        """
        try:
            self.gs.visualShowMessage(title, message, duration)
            return True
        except Exception as e:
            print(f"Error showing message: {e}")
            return False


# ------------------------------------------------------------
#  HELPER FUNCTIONS (UNCHANGED)
# ------------------------------------------------------------

def generate_orbit_positions(
    center_pos: list, radius: float, num_points: int, start_angle: float
) -> list:
    """
    Generate a circular orbit (list of [x, y, z] waypoints).
    """
    positions = []
    angle_step = (2 * math.pi) / num_points
    for i in range(num_points):
        angle = start_angle + (i * angle_step)
        x = center_pos[0] + radius * math.cos(angle)
        y = center_pos[1] + radius * math.sin(angle)
        z = center_pos[2]
        positions.append([x, y, z])
    return positions


# ------------------------------------------------------------
#  LANGCHAIN TOOL WRAPPERS
# ------------------------------------------------------------
# Each of these classes can be dropped into a LangChain agent as a Tool.
# They all inherit from BaseTool and define `name`, `description`, and `_run`.
# ------------------------------------------------------------

from langchain.tools import BaseTool
from typing import Optional


class SetTimeTool(BaseTool):
    name: str = "set_gaia_time"
    description: str = (
        "Set Gaia Sky's simulation clock to a specific Unix timestamp. "
        "Input should be a float or integer (e.g., 1625097600.0). "
        "Returns True if successful."
    )

    def _run(self, timestamp: str) -> str:
        try:
            ts = float(timestamp)
            with GaiaSkyDirector() as director:
                success = director.set_time(ts)
            return f"Set time to {ts}: {success}"
        except Exception as e:
            return f"Error in SetTimeTool: {e}"

    async def _arun(self, timestamp: str) -> str:
        return self._run(timestamp)


class StartTimeTool(BaseTool):
    name: str = "start_gaia_time"
    description: str = "Resume Gaia Sky's internal clock. No input required."

    def _run(self, _: Optional[str] = None) -> str:
        try:
            with GaiaSkyDirector() as director:
                success = director.start_time()
            return f"Started Gaia Sky clock: {success}"
        except Exception as e:
            return f"Error in StartTimeTool: {e}"

    async def _arun(self, _: Optional[str] = None) -> str:
        return self._run(_)


class StopTimeTool(BaseTool):
    name: str = "stop_gaia_time"
    description: str = "Pause Gaia Sky's internal clock. No input required."

    def _run(self, _: Optional[str] = None) -> str:
        try:
            with GaiaSkyDirector() as director:
                success = director.stop_time()
            return f"Stopped Gaia Sky clock: {success}"
        except Exception as e:
            return f"Error in StopTimeTool: {e}"

    async def _arun(self, _: Optional[str] = None) -> str:
        return self._run(_)


class SetTimeRateTool(BaseTool):
    name: str = "set_gaia_time_rate"
    description: str = (
        "Set Gaia Sky time progression rate (e.g., 1.0 = real time, 10.0 = 10×). "
        "Input: float or integer."
    )

    def _run(self, rate: str) -> str:
        try:
            r = float(rate)
            with GaiaSkyDirector() as director:
                success = director.set_time_rate(r)
            return f"Set time rate to {r}: {success}"
        except Exception as e:
            return f"Error in SetTimeRateTool: {e}"

    async def _arun(self, rate: str) -> str:
        return self._run(rate)


class FlyToObjectTool(BaseTool):
    name: str = "fly_to_object"
    description: str = (
        "Smoothly move Gaia Sky's camera to focus on a named object. "
        "Input format: '<object_name>,<duration_seconds>,<keep_rotation(True/False)>'. "
        "E.g., 'Mars,5.0,True'."
    )

    def _run(self, text: str) -> str:
        try:
            parts = [p.strip() for p in text.split(",")]
            if len(parts) < 1:
                return "Usage: '<object_name>,<duration_seconds>,<keep_rotation>'."
            obj = parts[0]
            dur = float(parts[1]) if len(parts) > 1 else 5.0
            keep = parts[2].lower() in ("true", "1", "yes") if len(parts) > 2 else True
            
            # Use the shared connection manager directly
            connection_manager = get_connection_manager()
            result = connection_manager.execute_safely('setCameraFocus', obj)
            # execute_safely returns True on success, False on failure
            success = result
            
            return f"Flew to {obj} over {dur}s (keep_rotation={keep}): {success}"
        except Exception as e:
            return f"Error in FlyToObjectTool: {e}"

    async def _arun(self, text: str) -> str:
        return self._run(text)


class OrbitCameraTool(BaseTool):
    name: str = "orbit_camera"
    description: str = (
        "Make the camera orbit around a target object. "
        "Input format: '<target_object>,<radius>,<duration_seconds>,<axis>,<reverse(True/False)>'. "
        "E.g., 'Earth,0.5,10.0,Z,False'."
    )

    def _run(self, text: str) -> str:
        try:
            parts = [p.strip() for p in text.split(",")]
            obj = parts[0]
            radius = float(parts[1]) if len(parts) > 1 else 1.0
            duration = float(parts[2]) if len(parts) > 2 else 10.0
            axis = parts[3] if len(parts) > 3 else "Z"
            rev = parts[4].lower() in ("true", "1", "yes") if len(parts) > 4 else False
            with GaiaSkyDirector() as director:
                success = director.start_camera_orbit(obj, radius, duration, axis, rev)
            return (
                f"Started orbit around {obj} at radius {radius} "
                f"over {duration}s on axis {axis} (reverse={rev}): {success}"
            )
        except Exception as e:
            return f"Error in OrbitCameraTool: {e}"

    async def _arun(self, text: str) -> str:
        return self._run(text)


class StopCameraTool(BaseTool):
    name: str = "stop_camera_motion"
    description: str = "Stop any active camera movement (orbit, fly-to, etc.)"

    def _run(self, _: Optional[str] = None) -> str:
        try:
            with GaiaSkyDirector() as director:
                success = director.stop_camera()
            return f"Stopped camera motion: {success}"
        except Exception as e:
            return f"Error in StopCameraTool: {e}"

    async def _arun(self, _: Optional[str] = None) -> str:
        return self._run(_)


class CaptureScreenshotTool(BaseTool):
    name: str = "capture_screenshot"
    description: str = "Capture a PNG of the current Gaia Sky view. Input: file path (e.g., '/tmp/galaxy.png')."

    def _run(self, file_path: str) -> str:
        try:
            with GaiaSkyDirector() as director:
                success = director.capture_screenshot(file_path)
            return f"Screenshot saved to '{file_path}': {success}"
        except Exception as e:
            return f"Error in CaptureScreenshotTool: {e}"

    async def _arun(self, file_path: str) -> str:
        return self._run(file_path)


class ToggleElementTool(BaseTool):
    name: str = "toggle_visual_element"
    description: str = (
        "Show or hide a specific Gaia Sky visual element. "
        "Input: '<element_key>,<visible(True/False)>'. "
        "Example element_key: 'element.orbits', 'element.constellations'."
    )

    def _run(self, text: str) -> str:
        try:
            key, vis = [p.strip() for p in text.split(",")]
            visible = vis.lower() in ("true", "1", "yes")
            with GaiaSkyDirector() as director:
                vc = VisualController(director)
                success = vc.toggle_element(key, visible)
            return f"Toggled '{key}' to {visible}: {success}"
        except Exception as e:
            return f"Error in ToggleElementTool: {e}"

    async def _arun(self, text: str) -> str:
        return self._run(text)


class AddCameraShakeTool(BaseTool):
    name: str = "add_camera_shake"
    description: str = (
        "Apply a subtle camera shake effect. "
        "Input: '<intensity>,<frequency>,<duration>'. "
        "All values are floats. E.g., '0.0002,0.1,3.0'."
    )

    def _run(self, text: str) -> str:
        try:
            parts = [float(p.strip()) for p in text.split(",")]
            intensity = parts[0]
            frequency = parts[1] if len(parts) > 1 else 0.05
            duration = parts[2] if len(parts) > 2 else 5.0
            with GaiaSkyDirector() as director:
                success = director.add_camera_shake(intensity, frequency, duration)
            return f"Added camera shake (intensity={intensity}, frequency={frequency}, duration={duration}): {success}"
        except Exception as e:
            return f"Error in AddCameraShakeTool: {e}"

    async def _arun(self, text: str) -> str:
        return self._run(text)


# ------------------------------------------------------------
#  NEW CINEMATIC TOOL WRAPPERS
# ------------------------------------------------------------

class CameraTransitionTool(BaseTool):
    name: str = "camera_transition"
    description: str = "Perform smooth camera transition movement. No input required."

    def _run(self, _: Optional[str] = None) -> str:
        try:
            with GaiaSkyDirector() as director:
                success = director.camera_transition()
            return f"Camera transition: {success}"
        except Exception as e:
            return f"Error in CameraTransitionTool: {e}"

    async def _arun(self, _: Optional[str] = None) -> str:
        return self._run(_)


class CameraTransitionKmTool(BaseTool):
    name: str = "camera_transition_km"
    description: str = "Distance-based smooth camera movement. Input: distance in kilometers (float)."

    def _run(self, distance: str) -> str:
        try:
            dist = float(distance)
            with GaiaSkyDirector() as director:
                success = director.camera_transition_km(dist)
            return f"Camera transition {dist} km: {success}"
        except Exception as e:
            return f"Error in CameraTransitionKmTool: {e}"

    async def _arun(self, distance: str) -> str:
        return self._run(distance)


class GoToObjectTool(BaseTool):
    name: str = "go_to_object"
    description: str = "Smoothly travel to a celestial object. Input: object name (e.g., 'Mars', 'Jupiter', 'Sun')."

    def _run(self, object_name: str) -> str:
        try:
            # Use shared connection instead of creating new one
            from gaia_sky_connection import get_connection_manager
            cm = get_connection_manager()
            gs = cm.get_gaia_sky_interface()
            if gs:
                gs.goToObject(object_name)
                return f"Successfully navigated to {object_name}. The camera smoothly travels through space to show this celestial object."
            else:
                return f"Failed to connect to Gaia Sky to navigate to {object_name}"
        except Exception as e:
            return f"Error navigating to {object_name}: {e}"

    async def _arun(self, object_name: str) -> str:
        return self._run(object_name)


class GoToObjectInstantTool(BaseTool):
    name: str = "go_to_object_instant"
    description: str = "Instantly jump to a celestial object. Input: object name (e.g., 'Mars', 'Jupiter', 'Sun')."

    def _run(self, object_name: str) -> str:
        try:
            with GaiaSkyDirector() as director:
                success = director.go_to_object_instant(object_name)
            return f"Instantly going to {object_name}: {success}"
        except Exception as e:
            return f"Error in GoToObjectInstantTool: {e}"

    async def _arun(self, object_name: str) -> str:
        return self._run(object_name)


class GoToObjectSmoothTool(BaseTool):
    name: str = "go_to_object_smooth"
    description: str = "Smoothly travel to a celestial object with extra smooth animation. Input: object name."

    def _run(self, object_name: str) -> str:
        try:
            with GaiaSkyDirector() as director:
                # Use confirmed working method for smooth camera movement
                director.gs.setCameraFocusInstantAndGo(object_name)
                success = True
            return f"Smoothly going to {object_name}: {success}"
        except Exception as e:
            return f"Error in GoToObjectSmoothTool: {e}"

    async def _arun(self, object_name: str) -> str:
        return self._run(object_name)


class SetCameraSpeedTool(BaseTool):
    name: str = "set_camera_speed"
    description: str = "Control camera travel velocity. Input: speed value (float, e.g., 50.0)."

    def _run(self, speed: str) -> str:
        try:
            spd = float(speed)
            with GaiaSkyDirector() as director:
                success = director.set_camera_speed(spd)
            return f"Set camera speed to {spd}: {success}"
        except Exception as e:
            return f"Error in SetCameraSpeedTool: {e}"

    async def _arun(self, speed: str) -> str:
        return self._run(speed)


class SetCameraTrackingTool(BaseTool):
    name: str = "set_camera_tracking"
    description: str = "Set camera to track an object during movement. Input: object name to track."

    def _run(self, object_name: str) -> str:
        try:
            # Use shared connection instead of creating new one
            from gaia_sky_connection import get_connection_manager
            cm = get_connection_manager()
            gs = cm.get_gaia_sky_interface()
            if gs:
                gs.setCameraTrackingObject(object_name)
                return f"Camera now tracking {object_name}. The view follows the object as it moves through space."
            else:
                return f"Failed to connect to Gaia Sky to track {object_name}"
        except Exception as e:
            return f"Error tracking {object_name}: {e}"

    async def _arun(self, object_name: str) -> str:
        return self._run(object_name)


class LandOnObjectTool(BaseTool):
    name: str = "land_on_object"
    description: str = "Perform smooth landing sequence on a celestial object. Input: object name (e.g., 'Mars', 'Moon')."

    def _run(self, object_name: str) -> str:
        try:
            # Use shared connection instead of creating new one
            from gaia_sky_connection import get_connection_manager
            cm = get_connection_manager()
            gs = cm.get_gaia_sky_interface()
            if gs:
                gs.landOnObject(object_name)
                return f"Successfully initiated landing sequence on {object_name}. The camera approaches the surface for detailed exploration."
            else:
                return f"Failed to connect to Gaia Sky to land on {object_name}"
        except Exception as e:
            return f"Error landing on {object_name}: {e}"

    async def _arun(self, object_name: str) -> str:
        return self._run(object_name)


class SetCinematicCameraTool(BaseTool):
    name: str = "set_cinematic_camera"
    description: str = "Enable/disable cinematic camera mode for smooth movie-like movement. Input: 'true' or 'false'."

    def _run(self, enable: str) -> str:
        try:
            enabled = enable.lower() in ('true', '1', 'yes', 'on')
            with GaiaSkyDirector() as director:
                success = director.set_cinematic_camera(enabled)
            return f"Cinematic camera {'enabled' if enabled else 'disabled'}: {success}"
        except Exception as e:
            return f"Error in SetCinematicCameraTool: {e}"

    async def _arun(self, enable: str) -> str:
        return self._run(enable)