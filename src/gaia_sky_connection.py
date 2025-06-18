#!/usr/bin/env python3
"""
Minimal Gaia Sky Connection Manager for Standalone Remote Controller
Extracted from the main project - only what's needed for simple_remote.py
"""

import threading
from typing import Optional, Any
from py4j.java_gateway import JavaGateway


class UniversalSpaceConnectionManager:
    """
    Singleton connection manager for Gaia Sky.
    Minimal version for standalone remote controller.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._gateway: Optional[JavaGateway] = None
        self._gs: Optional[Any] = None
        self._connection_lock = threading.RLock()
        self._is_connected = False
        self._connection_attempts = 0
        self._max_connection_attempts = 3
        self._initialized = True
    
    def connect(self) -> bool:
        """
        Establish connection to Gaia Sky.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        with self._connection_lock:
            if self._is_connected and self._gateway and self._gs:
                return True
            
            # Close any existing connection first
            self._disconnect_internal()
            
            try:
                print(f"[ConnectionManager] Connecting to Gaia Sky (attempt {self._connection_attempts + 1})...")
                self._gateway = JavaGateway()
                self._gs = self._gateway.entry_point
                
                # Test the connection with a simple call
                self._test_connection()
                
                self._is_connected = True
                self._connection_attempts = 0
                print("[ConnectionManager] ✅ Connected to Gaia Sky successfully!")
                return True
                
            except Exception as e:
                print(f"[ConnectionManager] ❌ Connection failed: {e}")
                self._disconnect_internal()
                self._connection_attempts += 1
                return False
    
    def _test_connection(self):
        """Test if the connection is working by calling a simple method."""
        if self._gs:
            try:
                # This should return some value if connection is working
                result = hasattr(self._gs, 'setCameraFocus')
                if not result:
                    raise Exception("Gaia Sky interface not available")
            except Exception as e:
                raise Exception(f"Connection test failed: {e}")
    
    def disconnect(self):
        """Disconnect from Gaia Sky."""
        with self._connection_lock:
            self._disconnect_internal()
    
    def _disconnect_internal(self):
        """Internal disconnect method without locking."""
        try:
            if self._gateway:
                self._gateway.close()
                print("[ConnectionManager] 🔌 Disconnected from Gaia Sky")
        except Exception as e:
            print(f"[ConnectionManager] Warning during disconnect: {e}")
        finally:
            self._gateway = None
            self._gs = None
            self._is_connected = False
    
    def get_gaia_sky_interface(self) -> Optional[Any]:
        """
        Get the Gaia Sky interface object.
        
        Returns:
            Gaia Sky interface object if connected, None otherwise
        """
        with self._connection_lock:
            if not self._is_connected:
                if not self.connect():
                    return None
            return self._gs
    
    def is_connected(self) -> bool:
        """Check if currently connected to Gaia Sky."""
        return self._is_connected and self._gateway is not None and self._gs is not None


# Global instance for easy access
connection_manager = UniversalSpaceConnectionManager()


def get_connection_manager() -> UniversalSpaceConnectionManager:
    """Get the global connection manager instance."""
    return connection_manager