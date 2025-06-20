#!/usr/bin/env python3
"""
🔍 GAIA SKY API DISCOVERY TOOL
Discover all available methods in the connected Gaia Sky instance
to find replacement for waitFocus() navigation completion detection
"""

import sys
import os
from py4j.java_gateway import JavaGateway

def discover_gaia_methods():
    """Discover all available methods in Gaia Sky interface"""
    
    print("🔍 GAIA SKY API DISCOVERY")
    print("=" * 50)
    
    try:
        print("🔌 Connecting to Gaia Sky...")
        gateway = JavaGateway()
        gs = gateway.entry_point
        
        print("✅ Connected! Discovering available methods...")
        
        # Get all available methods
        all_methods = dir(gs)
        print(f"📊 Total methods found: {len(all_methods)}")
        
        # Filter for navigation/completion related methods
        navigation_keywords = [
            'wait', 'focus', 'camera', 'position', 'state', 'status', 
            'complete', 'ready', 'busy', 'navigation', 'moving', 'target',
            'current', 'get', 'is', 'check', 'monitor', 'track'
        ]
        
        navigation_methods = []
        for method in all_methods:
            method_lower = method.lower()
            if any(keyword in method_lower for keyword in navigation_keywords):
                navigation_methods.append(method)
        
        print(f"\n🎯 NAVIGATION/STATE RELATED METHODS ({len(navigation_methods)} found):")
        print("-" * 60)
        
        for i, method in enumerate(sorted(navigation_methods), 1):
            print(f"{i:2d}. {method}")
        
        # Try to get method signatures for promising ones
        print(f"\n🔬 TESTING PROMISING METHODS:")
        print("-" * 40)
        
        promising_methods = [
            'waitFocus', 'isBusy', 'isReady', 'getState', 'getCameraState',
            'getCameraPosition', 'getFocusObject', 'getCurrentFocus',
            'isNavigating', 'getNavigationState', 'getCameraFocus',
            'getTarget', 'getCurrentTarget', 'isMoving', 'checkReady'
        ]
        
        available_promising = []
        for method in promising_methods:
            if method in all_methods:
                available_promising.append(method)
                print(f"✅ {method} - AVAILABLE")
                
                # Try to call method if it looks safe (no parameters)
                try:
                    if method.startswith(('get', 'is', 'check')) and method != 'getState':
                        result = getattr(gs, method)()
                        print(f"   └─ Returns: {result} (type: {type(result).__name__})")
                except Exception as e:
                    print(f"   └─ Call failed: {str(e)[:50]}...")
            else:
                print(f"❌ {method} - NOT AVAILABLE")
        
        print(f"\n🎯 CAMERA RELATED METHODS:")
        print("-" * 30)
        camera_methods = [m for m in all_methods if 'camera' in m.lower()]
        for method in sorted(camera_methods):
            print(f"📹 {method}")
            
        print(f"\n🎯 FOCUS RELATED METHODS:")
        print("-" * 30)
        focus_methods = [m for m in all_methods if 'focus' in m.lower()]
        for method in sorted(focus_methods):
            print(f"🎯 {method}")
        
        print(f"\n🎯 GET/IS/CHECK METHODS (State queries):")
        print("-" * 40)
        state_methods = [m for m in all_methods if m.startswith(('get', 'is', 'check', 'has'))]
        for method in sorted(state_methods[:20]):  # Show first 20
            print(f"📊 {method}")
        if len(state_methods) > 20:
            print(f"... and {len(state_methods) - 20} more")
        
        # Test camera position monitoring
        print(f"\n🧪 TESTING CAMERA POSITION MONITORING:")
        print("-" * 40)
        
        if 'getCameraPosition' in all_methods:
            try:
                pos1 = gs.getCameraPosition()
                print(f"📍 Camera Position: {pos1}")
                print(f"   Type: {type(pos1)}")
                if hasattr(pos1, '__len__'):
                    print(f"   Length: {len(pos1)}")
                    if len(pos1) >= 3:
                        print(f"   X,Y,Z: {pos1[0]}, {pos1[1]}, {pos1[2]}")
            except Exception as e:
                print(f"❌ getCameraPosition failed: {e}")
        
        if 'getFocusObject' in all_methods:
            try:
                focus = gs.getFocusObject()
                print(f"🎯 Focus Object: {focus}")
            except Exception as e:
                print(f"❌ getFocusObject failed: {e}")
                
        if 'getCameraFocus' in all_methods:
            try:
                focus = gs.getCameraFocus()
                print(f"🎯 Camera Focus: {focus}")
            except Exception as e:
                print(f"❌ getCameraFocus failed: {e}")
        
        print(f"\n✅ DISCOVERY COMPLETE!")
        print(f"💡 Available promising methods: {len(available_promising)}")
        print(f"📋 Check output above for suitable waitFocus() replacement")
        
        gateway.close()
        
    except Exception as e:
        print(f"❌ Discovery failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    discover_gaia_methods()