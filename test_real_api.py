#!/usr/bin/env python3
"""
Test Real API Integration
Quick test to verify that real Gaia Sky API methods are working
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.config import setup_project_path, setup_logger
from remote_controller import SpaceNavigationController
from gaia_sky_methods import get_method_registry

# Setup project path and logging
setup_project_path()
logger = setup_logger(__name__)

def test_real_api_integration():
    """Test the real API integration"""
    
    print("🧪 TESTING REAL GAIA SKY API INTEGRATION")
    print("=" * 50)
    
    # Initialize controller
    print("1️⃣ Initializing controller...")
    controller = SpaceNavigationController()
    registry = get_method_registry()
    
    print(f"✅ Controller initialized")
    print(f"✅ Method registry loaded with {len(registry.get_all_method_names())} methods")
    
    # Test connection
    print("\n2️⃣ Testing Gaia Sky connection...")
    try:
        if controller.connect():
            print("✅ Successfully connected to Gaia Sky!")
            
            # Test getting interface
            gs, error = controller._get_gaia_sky_interface_with_validation()
            if gs:
                print("✅ Gaia Sky interface accessible")
                
                # Test method validation
                print("\n3️⃣ Testing method validation...")
                essential_methods = [
                    'goToObject', 'goToObjectSmooth', 'setCameraFocus', 
                    'takeScreenshot', 'cameraStop', 'landOnObject'
                ]
                
                available_count = 0
                for method in essential_methods:
                    if registry.validate_method_call(gs, method):
                        print(f"✅ {method} - Available")
                        available_count += 1
                    else:
                        print(f"❌ {method} - Not available")
                
                print(f"\n📊 {available_count}/{len(essential_methods)} essential methods available")
                
                # Test current state
                print("\n4️⃣ Testing current state retrieval...")
                state = controller.get_current_state()
                if state.get('connected'):
                    print("✅ Current state retrieved successfully")
                    print(f"   Camera position: {state.get('camera_position', 'Unknown')}")
                    print(f"   Last target: {state.get('last_target', 'None')}")
                else:
                    print(f"❌ State retrieval failed: {state.get('error', 'Unknown error')}")
                
                # Test simple command
                print("\n5️⃣ Testing real command execution...")
                print("   Executing: 'take screenshot'")
                result = controller.execute_command("take screenshot")
                print(f"   Result: {result}")
                
                if "✅" in result or "📸" in result:
                    print("✅ Real API command executed successfully!")
                else:
                    print("❌ Command execution may have failed")
                
            else:
                print(f"❌ Cannot access Gaia Sky interface: {error}")
        else:
            print("❌ Failed to connect to Gaia Sky")
            print("💡 Make sure Gaia Sky is running with Python bridge enabled")
            print("💡 Check that port 25333 is accessible")
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
    
    finally:
        try:
            controller.disconnect()
            print("\n🔌 Disconnected from Gaia Sky")
        except:
            pass
    
    print("\n" + "=" * 50)
    print("🎯 REAL API INTEGRATION TEST COMPLETE")
    print("💡 If methods show as 'Not available', check your Gaia Sky version")
    print("💡 The controller will gracefully handle missing methods")

if __name__ == "__main__":
    test_real_api_integration()