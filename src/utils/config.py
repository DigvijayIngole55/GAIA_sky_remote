"""
Configuration constants for the Astro Remote Controller
"""

import os
import sys
import logging

# Speech Recognition Configuration
WHISPER_MODEL_SIZE = "base"  # tiny, base, small, medium, large
SAMPLE_RATE = 16000  # Hz
CHUNK_DURATION = 4.0  # seconds (longer to capture full ASTRO commands)
MIN_SPEECH_LENGTH = 1  # minimum words to process (reduced to capture short commands)

# LM Studio Configuration
LM_STUDIO_BASE_URL = "http://localhost:1234/v1"
LM_STUDIO_MODEL = "google/gemma-3-4b-it"
LM_STUDIO_TIMEOUT = 10  # seconds
LM_STUDIO_TEMPERATURE = 0.1
LM_STUDIO_MAX_TOKENS = 100

# Gaia Sky Configuration
GAIA_SKY_RETRY_ATTEMPTS = 3
GAIA_SKY_RETRY_DELAY = 2.0  # seconds

# Audio Configuration
AUDIO_FORMAT = "paInt16"
AUDIO_CHANNELS = 1
AUDIO_FRAMES_PER_BUFFER = 1024

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# TTS Configuration
TTS_ENABLED = True
TTS_ENGINE = "pyttsx3"  # Currently only pyttsx3 supported
TTS_RATE = 180  # words per minute (normal speech)
TTS_URGENT_RATE = 220  # words per minute (urgent commands)
TTS_VOICE_INDEX = 0  # system voice selection (0 = default)

# Environment Variable Overrides
def get_env_config():
    """Get configuration from environment variables"""
    return {
        "WHISPER_MODEL_SIZE": os.getenv("ASTRO_WHISPER_MODEL", WHISPER_MODEL_SIZE),
        "LM_STUDIO_BASE_URL": os.getenv("ASTRO_LM_STUDIO_URL", LM_STUDIO_BASE_URL),
        "LM_STUDIO_MODEL": os.getenv("ASTRO_LM_STUDIO_MODEL", LM_STUDIO_MODEL),
        "LOG_LEVEL": os.getenv("ASTRO_LOG_LEVEL", LOG_LEVEL),
    }

# Available Actions
AVAILABLE_ACTIONS = [
    # Phase 1: Core methods (18 methods)
    'go_to', 'land_on', 'track', 'set_time', 'take_screenshot', 
    'explore', 'orbit', 'zoom_in', 'zoom_out', 'speed_up', 
    'slow_down', 'free_camera', 'stop_camera', 'back_to_space', 
    'tour', 'cinematic_journey', 'multi_step', 'stream_tour',
    
    # Phase 2: Advanced new methods (7 methods)
    'camera_transition', 'draw_path', 'add_marker', 'time_travel',
    'pitch_camera', 'roll_camera', 'smooth_orientation'
]

# Common Celestial Objects
CELESTIAL_OBJECTS = [
    'Mars', 'Earth', 'Moon', 'Jupiter', 'Saturn', 'Sun', 'Venus', 
    'Mercury', 'Neptune', 'Uranus', 'Pluto', 'Alpha Centauri', 
    'Betelgeuse', 'Vega', 'Sirius', 'ISS', 'Hubble'
]

# Tour Routes
TOUR_ROUTES = {
    "solar system": ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
    "planets": ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
    "inner planets": ["Mercury", "Venus", "Earth", "Mars"],
    "outer planets": ["Jupiter", "Saturn", "Uranus", "Neptune"],
    "gas giants": ["Jupiter", "Saturn", "Uranus", "Neptune"],
    "terrestrial planets": ["Mercury", "Venus", "Earth", "Mars"],
    "jupiter moons": ["Io", "Europa", "Ganymede", "Callisto"],
    "saturn moons": ["Titan", "Enceladus", "Mimas", "Iapetus"]
}

# Common Utility Functions
def setup_project_path():
    """Add src directory to Python path for imports"""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    src_path = os.path.join(project_root, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

def setup_logger(name: str, level: str = None) -> logging.Logger:
    """Setup standardized logger for the project"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, level or LOG_LEVEL))
    return logger