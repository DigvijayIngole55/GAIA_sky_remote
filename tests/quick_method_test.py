#!/usr/bin/env python3
"""
🚀 QUICK METHOD TEST - Automated
Test all 18 methods without user input to verify fixes
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from remote_controller import SpaceNavigationController
import time

def quick_test_all_methods():
    """Quick automated test of all 18 methods"""
    
    print("🚀 QUICK TEST: All 25 Methods (18 Phase 1 + 7 Phase 2)")
    print("=" * 60)
    
    # Initialize controller
    controller = SpaceNavigationController()
    
    # Connect to Gaia Sky
    if not controller.connect():
        print("❌ Failed to connect to Gaia Sky")
        return
    
    print("✅ Connected to Gaia Sky")
    
    # Test all methods with simple parameters
    test_methods = [
        ('go_to', 'Mars', {}),
        ('land_on', 'Moon', {}),
        ('track', 'Saturn', {}),
        ('explore', 'Venus', {}),
        ('take_screenshot', '', {}),
        ('set_time', '', {'year': 2030}),
        ('free_camera', '', {}),
        ('stop_camera', '', {}),
        ('back_to_space', '', {}),
        ('orbit', 'Earth', {}),
        ('zoom_in', '', {}),
        ('zoom_out', '', {}),
        ('speed_up', '', {}),
        ('slow_down', '', {}),
        ('tour', 'inner planets', {}),
        ('cinematic_journey', 'Jupiter', {'duration': 3.0}),
        ('multi_step', 'Mars', {'steps': [{'action': 'go_to', 'entity': 'Mars'}], 'delay': 0.5}),
        ('stream_tour', 'Saturn', {'duration': 3.0})
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for i, (method_name, entity, params) in enumerate(test_methods, 1):
        print(f"\n🧪 TEST {i}/18: {method_name.upper()}")
        try:
            start_time = time.time()
            method = controller.action_map[method_name]
            result = method(entity, params)
            execution_time = time.time() - start_time
            
            success = not result.startswith("❌")
            status = "✅ PASS" if success else "❌ FAIL"
            
            print(f"   {status} ({execution_time:.2f}s)")
            if success:
                passed += 1
            else:
                failed += 1
                print(f"   Error: {result[:80]}...")
            
            results.append((method_name, success, execution_time, result))
            
            # Small delay between tests
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ❌ EXCEPTION: {e}")
            failed += 1
            results.append((method_name, False, 0, str(e)))
    
    # Summary
    print(f"\n" + "=" * 50)
    print(f"📊 QUICK TEST SUMMARY")
    print(f"=" * 50)
    print(f"✅ Passed: {passed}/18")
    print(f"❌ Failed: {failed}/18")
    print(f"📈 Success Rate: {(passed/18*100):.1f}%")
    
    if failed == 0:
        print(f"🎉 ALL METHODS WORKING PERFECTLY!")
    else:
        print(f"⚠️  {failed} methods still need attention:")
        for method_name, success, _, result in results:
            if not success:
                print(f"  • {method_name}: {result[:60]}...")
    
    controller.disconnect()
    return passed == 18

if __name__ == "__main__":
    success = quick_test_all_methods()
    sys.exit(0 if success else 1)