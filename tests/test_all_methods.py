#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE METHOD TESTING
Test all 18 LLM agent methods to verify they work correctly
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from utils.config import setup_project_path, setup_logger
from remote_controller import SpaceNavigationController
import logging

# Setup logging to see all details
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
setup_project_path()

class MethodTester:
    """Comprehensive testing of all controller methods"""
    
    def __init__(self):
        self.controller = None
        self.test_results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def setup(self):
        """Initialize controller and connect to Gaia Sky"""
        print("🔧 SETUP: Initializing controller...")
        self.controller = SpaceNavigationController()
        
        print("🔌 SETUP: Connecting to Gaia Sky...")
        if not self.controller.connect():
            print("❌ SETUP FAILED: Cannot connect to Gaia Sky")
            print("💡 Make sure Gaia Sky is running with Python bridge enabled")
            return False
        
        print("✅ SETUP COMPLETE: Connected to Gaia Sky")
        return True
    
    def test_method(self, method_name, entity="", params=None, description=""):
        """Test a single method and record results"""
        if params is None:
            params = {}
            
        self.total_tests += 1
        test_num = self.total_tests
        
        print(f"\n{'='*60}")
        print(f"🧪 TEST {test_num}: {method_name.upper()}")
        print(f"📝 Description: {description}")
        print(f"🎯 Entity: '{entity}', Params: {params}")
        print(f"{'='*60}")
        
        try:
            # Get the method from action_map
            if method_name not in self.controller.action_map:
                result = f"❌ Method '{method_name}' not found in action_map"
                self.record_result(method_name, False, result)
                return
            
            method = self.controller.action_map[method_name]
            
            # Execute the method
            start_time = time.time()
            result = method(entity, params)
            execution_time = time.time() - start_time
            
            # Analyze result
            success = not (result.startswith("❌") or "failed" in result.lower())
            
            print(f"⏱️  Execution Time: {execution_time:.2f}s")
            print(f"📤 Result: {result}")
            
            if success:
                print(f"✅ TEST {test_num} PASSED")
                self.passed_tests += 1
            else:
                print(f"❌ TEST {test_num} FAILED")
                self.failed_tests += 1
                
            self.record_result(method_name, success, result, execution_time)
            
            # Small delay between tests to prevent overwhelming Gaia Sky
            time.sleep(1)
            
        except Exception as e:
            execution_time = time.time() - start_time if 'start_time' in locals() else 0
            error_result = f"❌ EXCEPTION: {str(e)}"
            print(f"💥 EXCEPTION in {method_name}: {e}")
            print(f"❌ TEST {test_num} FAILED")
            self.failed_tests += 1
            self.record_result(method_name, False, error_result, execution_time)
    
    def record_result(self, method_name, success, result, execution_time=0):
        """Record test result for reporting"""
        self.test_results[method_name] = {
            'success': success,
            'result': result,
            'execution_time': execution_time
        }
    
    def run_all_tests(self):
        """Execute comprehensive tests for all 18 methods"""
        
        print("🚀 STARTING COMPREHENSIVE METHOD TESTING")
        print("=" * 80)
        
        # 1. NAVIGATION METHODS
        print("\n🧭 CATEGORY 1: NAVIGATION METHODS")
        print("-" * 40)
        
        self.test_method('go_to', 'Mars', {'smooth': True, 'duration': 3.0}, 
                        "Basic navigation to Mars with smooth movement")
        
        self.test_method('go_to', 'Moon', {'instant': True}, 
                        "Instant navigation to Moon")
        
        self.test_method('land_on', 'Moon', {'latitude': 20.0, 'longitude': -15.0}, 
                        "Land on Moon with specific coordinates")
        
        self.test_method('track', 'Saturn', {}, 
                        "Track Saturn with camera")
        
        self.test_method('explore', 'Venus', {}, 
                        "Cinematic exploration of Venus")
        
        self.test_method('orbit', 'Earth', {'distance': 5.0, 'speed': 0.8}, 
                        "Orbit around Earth at 5x distance")
        
        # 2. CAMERA CONTROL METHODS  
        print("\n📹 CATEGORY 2: CAMERA CONTROL METHODS")
        print("-" * 40)
        
        self.test_method('zoom_in', '', {'factor': 2.0}, 
                        "Zoom camera in by 2x factor")
        
        self.test_method('zoom_out', '', {'factor': 0.5}, 
                        "Zoom camera out by 0.5x factor")
        
        self.test_method('free_camera', '', {}, 
                        "Free camera from constraints")
        
        self.test_method('stop_camera', '', {}, 
                        "Stop all camera movement")
        
        self.test_method('back_to_space', '', {}, 
                        "Move camera back to space")
        
        # 3. UTILITY METHODS
        print("\n🛠️  CATEGORY 3: UTILITY METHODS")
        print("-" * 40)
        
        self.test_method('take_screenshot', '', {'width': 1920, 'height': 1080}, 
                        "Take high-resolution screenshot")
        
        self.test_method('set_time', '', {'year': 2030, 'month': 7, 'day': 4, 'hour': 15}, 
                        "Set simulation time to July 4, 2030, 3 PM")
        
        self.test_method('speed_up', '', {'factor': 3.0}, 
                        "Increase simulation speed by 3x")
        
        self.test_method('slow_down', '', {'factor': 0.5}, 
                        "Decrease simulation speed to 0.5x")
        
        # 4. ADVANCED MULTI-STEP METHODS
        print("\n🎬 CATEGORY 4: ADVANCED MULTI-STEP METHODS")
        print("-" * 40)
        
        self.test_method('tour', 'inner planets', {'delay': 2.0, 'smooth': True}, 
                        "Tour of inner planets with 2s delays")
        
        self.test_method('cinematic_journey', 'Jupiter', {'duration': 6.0, 'effects': True}, 
                        "Cinematic journey to Jupiter with effects")
        
        # Multi-step test with sequence of commands
        multi_step_params = {
            'steps': [
                {'action': 'go_to', 'entity': 'Mars'},
                {'action': 'take_screenshot', 'entity': ''},
                {'action': 'zoom_in', 'entity': '', 'parameters': {'factor': 1.5}}
            ],
            'delay': 1.0,
            'stop_on_error': False
        }
        self.test_method('multi_step', 'Mars', multi_step_params, 
                        "Multi-step: Go to Mars → Screenshot → Zoom in")
        
        self.test_method('stream_tour', 'Jupiter', {'duration': 8.0, 'orbit_speed': 0.5}, 
                        "Stream tour around Jupiter for 8 seconds")
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        print(f"📈 Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📊 Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        print("-" * 50)
        
        # Group results by category
        categories = {
            'Navigation': ['go_to', 'land_on', 'track', 'explore', 'orbit'],
            'Camera Control': ['zoom_in', 'zoom_out', 'free_camera', 'stop_camera', 'back_to_space'],
            'Utilities': ['take_screenshot', 'set_time', 'speed_up', 'slow_down'],
            'Advanced Multi-step': ['tour', 'cinematic_journey', 'multi_step', 'stream_tour']
        }
        
        for category, methods in categories.items():
            print(f"\n📂 {category.upper()}:")
            for method in methods:
                if method in self.test_results:
                    result = self.test_results[method]
                    status = "✅ PASS" if result['success'] else "❌ FAIL"
                    time_str = f"({result['execution_time']:.2f}s)" if result['execution_time'] > 0 else ""
                    print(f"  {method:20} {status} {time_str}")
                    if not result['success']:
                        # Show first 80 chars of error
                        error_preview = result['result'][:80] + "..." if len(result['result']) > 80 else result['result']
                        print(f"    ↳ {error_preview}")
        
        print(f"\n🎯 PERFORMANCE METRICS:")
        print("-" * 30)
        total_time = sum(r['execution_time'] for r in self.test_results.values())
        avg_time = total_time / len(self.test_results) if self.test_results else 0
        print(f"Total Execution Time: {total_time:.2f}s")
        print(f"Average per Method: {avg_time:.2f}s")
        
        # Show methods that took longest
        longest_methods = sorted(self.test_results.items(), 
                                key=lambda x: x[1]['execution_time'], reverse=True)[:3]
        print(f"\n⏰ SLOWEST METHODS:")
        for method, result in longest_methods:
            print(f"  {method}: {result['execution_time']:.2f}s")
        
        print(f"\n🎉 TESTING COMPLETE!")
        if self.failed_tests == 0:
            print("🏆 ALL METHODS WORKING PERFECTLY!")
        else:
            print(f"⚠️  {self.failed_tests} methods need attention - see details above")
    
    def cleanup(self):
        """Cleanup and disconnect"""
        if self.controller:
            print("\n🔌 Disconnecting from Gaia Sky...")
            self.controller.disconnect()
            print("👋 Cleanup complete!")

def main():
    """Main test execution"""
    tester = MethodTester()
    
    try:
        if not tester.setup():
            return
        
        print("\n⚠️  IMPORTANT: This test will control Gaia Sky camera and navigation")
        print("🎮 You'll see the view change as each method is tested")
        print("⏰ Estimated time: 2-3 minutes for all 18 methods")
        
        input("\n📋 Press Enter to start comprehensive testing... ")
        
        tester.run_all_tests()
        tester.print_summary()
        
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main()