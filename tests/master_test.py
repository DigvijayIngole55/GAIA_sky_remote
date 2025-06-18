#!/usr/bin/env python3
"""
Master Test Suite for Remote Controller
Tests all tools, flows, and error scenarios systematically
"""

import time
import sys
import os
import argparse
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

# Import the remote controller
from remote_controller import SimpleRemoteController

@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    command: str
    success: bool
    execution_time: float
    result_message: str
    error_details: str = ""

class MasterTestSuite:
    """Comprehensive test suite for the remote controller"""
    
    def __init__(self):
        print("🧪 Initializing Master Test Suite...")
        self.controller = SimpleRemoteController()
        self.results: List[TestResult] = []
        self.connected = False
        
    def connect_to_gaia_sky(self) -> bool:
        """Test connection to Gaia Sky"""
        print("🔌 Testing Gaia Sky connection...")
        try:
            self.connected = self.controller.connect()
            if self.connected:
                print("✅ Connection successful!")
                return True
            else:
                print("❌ Connection failed!")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def run_test(self, test_name: str, command: str, expect_success: bool = True) -> TestResult:
        """Run a single test and record results"""
        print(f"\n🔬 Testing: {test_name}")
        print(f"   Command: '{command}'")
        
        start_time = time.perf_counter()
        
        try:
            result = self.controller.execute_command(command)
            execution_time = time.perf_counter() - start_time
            
            # Determine success based on result content
            success = ("✅" in result or "✈️" in result or "🛬" in result or 
                      "👁️" in result or "🌌" in result or "📸" in result or
                      "🔓" in result or "⏹️" in result or "🚀" in result or
                      "🎬" in result or "🎉" in result or "📺" in result) and "❌" not in result
            
            if expect_success and not success:
                success = False
                error_details = f"Expected success but got: {result}"
            elif not expect_success and success:
                success = False
                error_details = f"Expected failure but got success: {result}"
            else:
                error_details = ""
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   Result: {status} ({execution_time:.3f}s)")
            print(f"   Output: {result[:100]}..." if len(result) > 100 else f"   Output: {result}")
            
            test_result = TestResult(
                test_name=test_name,
                command=command,
                success=success,
                execution_time=execution_time,
                result_message=result,
                error_details=error_details
            )
            
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            error_msg = str(e)
            
            print(f"   Result: ❌ EXCEPTION ({execution_time:.3f}s)")
            print(f"   Error: {error_msg}")
            
            test_result = TestResult(
                test_name=test_name,
                command=command,
                success=False,
                execution_time=execution_time,
                result_message="",
                error_details=error_msg
            )
        
        self.results.append(test_result)
        return test_result
    
    def test_basic_navigation(self) -> None:
        """Test basic navigation commands"""
        print("\n" + "="*60)
        print("🚀 TESTING BASIC NAVIGATION TOOLS")
        print("="*60)
        
        nav_tests = [
            ("Go to Mars", "go to mars"),
            ("Go to Jupiter", "take me to jupiter"),
            ("Go to Alpha Centauri", "fly to alpha centauri"),
            ("Visit Saturn", "visit saturn"),
            ("Navigate to Venus", "navigate to venus"),
            ("Show me Pluto", "show me pluto"),
        ]
        
        for test_name, command in nav_tests:
            self.run_test(test_name, command)
            time.sleep(0.5)  # Brief pause between tests
    
    def test_landing_operations(self) -> None:
        """Test landing operations"""
        print("\n" + "="*60)
        print("🛬 TESTING LANDING OPERATIONS")
        print("="*60)
        
        landing_tests = [
            ("Land on Moon", "land on the moon"),
            ("Land on Mars", "land on mars"),
            ("Touch down on Europa", "touch down on europa"),
            ("Set down on Titan", "set down on titan"),
        ]
        
        for test_name, command in landing_tests:
            self.run_test(test_name, command)
            time.sleep(0.5)
    
    def test_tracking_operations(self) -> None:
        """Test object tracking"""
        print("\n" + "="*60)
        print("👁️ TESTING TRACKING OPERATIONS")
        print("="*60)
        
        tracking_tests = [
            ("Track Saturn", "track saturn"),
            ("Follow Jupiter", "follow jupiter"),
            ("Watch the Moon", "watch the moon"),
            ("Focus on Venus", "focus on venus"),
        ]
        
        for test_name, command in tracking_tests:
            self.run_test(test_name, command)
            time.sleep(0.5)
    
    def test_exploration_modes(self) -> None:
        """Test exploration and cinematic modes"""
        print("\n" + "="*60)
        print("🌌 TESTING EXPLORATION MODES")
        print("="*60)
        
        exploration_tests = [
            ("Explore Venus", "explore venus"),
            ("Investigate Mars", "investigate mars"),
            ("Examine Jupiter", "examine jupiter"),
            ("Study Saturn", "study saturn"),
        ]
        
        for test_name, command in exploration_tests:
            self.run_test(test_name, command)
            time.sleep(0.5)
    
    def test_camera_controls(self) -> None:
        """Test camera and control operations"""
        print("\n" + "="*60)
        print("📷 TESTING CAMERA CONTROLS")
        print("="*60)
        
        camera_tests = [
            ("Take Screenshot", "take a screenshot"),
            ("Capture Image", "capture image"),
            ("Free Camera", "free camera"),
            ("Stop Camera", "stop camera"),
            ("Back to Space", "back to space"),
        ]
        
        for test_name, command in camera_tests:
            self.run_test(test_name, command)
            time.sleep(0.5)
    
    def test_complex_tours(self) -> None:
        """Test complex multi-step tours"""
        print("\n" + "="*60)
        print("🎬 TESTING COMPLEX TOURS & FLOWS")
        print("="*60)
        
        tour_tests = [
            ("Solar System Tour", "tour the solar system"),
            ("Planet Tour", "tour planets"),
            ("Inner Planets Tour", "tour inner planets"),
            ("Gas Giants Tour", "tour gas giants"),
            ("Cinematic Journey to Mars", "cinematic journey to mars"),
            ("Stream Tour of Jupiter", "stream tour of jupiter moons"),
        ]
        
        for test_name, command in tour_tests:
            self.run_test(test_name, command)
            time.sleep(1)  # Longer pause for complex operations
    
    def test_multi_step_commands(self) -> None:
        """Test multi-step command parsing"""
        print("\n" + "="*60)
        print("🔄 TESTING MULTI-STEP COMMANDS")
        print("="*60)
        
        multi_step_tests = [
            ("Visit Mars then Land", "visit mars then land on it"),
            ("Go to Jupiter and Track", "go to jupiter and track it"),
            ("Multi-step Mars", "go to mars then land on mars"),
        ]
        
        for test_name, command in multi_step_tests:
            self.run_test(test_name, command)
            time.sleep(1)
    
    def test_error_scenarios(self) -> None:
        """Test error handling and edge cases"""
        print("\n" + "="*60)
        print("⚠️ TESTING ERROR SCENARIOS")
        print("="*60)
        
        error_tests = [
            ("Invalid Object", "go to fakePlanet123", False),
            ("Empty Command", "", False),
            ("Gibberish Command", "xyzabc123 blahblah", False),
            ("Incomplete Command", "go to", False),
        ]
        
        for test_name, command, expect_success in error_tests:
            self.run_test(test_name, command, expect_success)
            time.sleep(0.5)
    
    def test_performance_timing(self) -> None:
        """Test performance of different command types"""
        print("\n" + "="*60)
        print("⏱️ TESTING PERFORMANCE TIMING")
        print("="*60)
        
        performance_tests = [
            ("Simple Command Speed", "go to mars"),
            ("Complex Command Speed", "cinematic journey to jupiter"),
            ("Tour Command Speed", "tour inner planets"),
        ]
        
        for test_name, command in performance_tests:
            # Run multiple times and average
            times = []
            for i in range(3):
                result = self.run_test(f"{test_name} (Run {i+1})", command)
                times.append(result.execution_time)
                time.sleep(0.2)
            
            avg_time = sum(times) / len(times)
            print(f"   📊 Average time for '{test_name}': {avg_time:.3f}s")
    
    def test_llm_vs_regex_fallback(self) -> None:
        """Test LLM parsing vs regex fallback"""
        print("\n" + "="*60)
        print("🧠 TESTING LLM vs REGEX PARSING")
        print("="*60)
        
        parsing_tests = [
            ("Clear Command (should use LLM)", "go to mars"),
            ("Natural Language", "take me on a journey to jupiter"),
            ("Casual Speech", "hey, can you show me saturn?"),
            ("Direct Command", "mars"),
        ]
        
        for test_name, command in parsing_tests:
            self.run_test(test_name, command)
            time.sleep(0.5)
    
    def test_natural_language_commands(self) -> None:
        """Test extensive natural language variations"""
        print("\n" + "="*60)
        print("🗣️ TESTING NATURAL LANGUAGE COMMANDS")
        print("="*60)
        
        natural_tests = [
            # Very casual navigation
            ("Casual Mars 1", "yo lets check out mars"),
            ("Casual Jupiter 1", "umm can we go to jupiter"),
            ("Casual Saturn 1", "oh saturn looks cool"),
            ("Casual Venus 1", "hey show me venus"),
            ("Casual Moon 1", "dude take me to the moon"),
            
            # Questions as commands
            ("Question Mars", "whats mars like"),
            ("Question Jupiter", "how big is jupiter"),
            ("Question Saturn", "what do saturn rings look like"),
            ("Question Venus", "is venus really that hot"),
            ("Question Moon", "can we see earth from the moon"),
            
            # Hesitant speech
            ("Hesitant Mars", "maybe we could go to mars"),
            ("Hesitant Jupiter", "i think jupiter would be cool"),
            ("Hesitant Saturn", "saturn might be interesting"),
            ("Hesitant Venus", "venus could be worth seeing"),
            ("Hesitant Moon", "the moon seems nice"),
            
            # Excited/emotional
            ("Excited Mars", "mars is so awesome"),
            ("Excited Jupiter", "jupiter must be incredible"),
            ("Excited Saturn", "saturn is beautiful"),
            ("Excited Venus", "venus looks mysterious"),
            ("Excited Moon", "the moon is amazing"),
            
            # With filler words
            ("Filler Mars", "like go to mars"),
            ("Filler Jupiter", "you know jupiter"),
            ("Filler Saturn", "so um saturn"),
            ("Filler Venus", "well venus"),
            ("Filler Moon", "uh the moon"),
            
            # Slang
            ("Slang Mars", "mars looks sick"),
            ("Slang Jupiter", "jupiter is mental"),
            ("Slang Saturn", "saturn is lit"),
            ("Slang Venus", "venus is fire"),
            ("Slang Moon", "moon vibes"),
            
            # Casual landing
            ("Casual Landing Moon", "can we actually land on the moon"),
            ("Casual Landing Mars", "i wanna touch down on mars"),
            ("Casual Landing Request", "lets land on the moon and walk around"),
            ("Casual Drop Off", "put me down on mars surface"),
            ("Simple Landing", "drop me off on the moon"),
            
            # Natural photo requests
            ("Natural Photo 1", "this looks amazing take a picture"),
            ("Natural Photo 2", "get a photo of this view"),
            ("Natural Photo 3", "save this its so beautiful"),
            ("Natural Photo 4", "capture this moment"),
            ("Natural Photo 5", "screenshot this please"),
            
            # Recovery - frustrated
            ("Frustrated Help 1", "help im stuck here"),
            ("Frustrated Help 2", "get me out of this mess"),
            ("Frustrated Help 3", "something went wrong fix it"),
            ("Frustrated Help 4", "the view is all weird"),
            ("Frustrated Help 5", "camera is acting up"),
            
            # Complex natural requests
            ("Complex Mars", "take me to mars and let me walk around"),
            ("Complex Jupiter", "i want to see jupiter then take a picture"),
            ("Complex Saturn", "show me saturn up close and personal"),
            ("Complex Venus", "venus tour would be awesome"),
            ("Complex Moon", "moon trip with landing please"),
            
            # Stream of consciousness
            ("Stream Mars", "so like mars is the red planet right and i really wanna see what it looks like"),
            ("Stream Jupiter", "jupiter is this massive gas giant and i bet the view is incredible"),
            ("Stream Saturn", "saturn has those crazy beautiful rings that must be amazing to see"),
            
            # Regional/dialectal
            ("Regional Mars", "reckon we could mosey on over to mars"),
            ("Regional Jupiter", "fancy a trip to jupiter mate"),
            ("Regional Saturn", "how bout we cruise to saturn"),
            ("Regional Venus", "lets mosey on down to venus"),
            ("Regional Moon", "wanna pop over to the moon"),
            
            # Technical but casual
            ("Tech Mars", "mars has that thin atmosphere right"),
            ("Tech Jupiter", "jupiter with the great red spot"),
            ("Tech Saturn", "saturn and those icy rings"),
            ("Tech Venus", "venus with the thick clouds"),
            ("Tech Moon", "moon with the low gravity"),
        ]
        
        for test_name, command in natural_tests:
            self.run_test(test_name, command)
            time.sleep(0.1)
    
    def test_realistic_simulation(self) -> None:
        """Test realistic usage simulation - chained actions to test robustness"""
        print("\n" + "="*60)
        print("🎮 TESTING REALISTIC USAGE SIMULATION")
        print("="*60)
        
        # Scenario 1: Mars exploration mission
        print("\n🚀 SCENARIO 1: Mars Exploration Mission")
        mars_mission = [
            ("Start Mission", "hey take me to mars"),
            ("Get Closer", "show me mars up close"),
            ("Land on Surface", "land on mars please"),
            ("Take Photo", "this is cool take a picture"),
            ("Get Stuck", "help im stuck"),
            ("Free Camera", "get me unstuck"),
            ("Back to Space", "get me back to space"),
        ]
        
        for test_name, command in mars_mission:
            self.run_test(f"Mars Mission - {test_name}", command)
            time.sleep(0.8)
        
        # Scenario 2: Tourist tour of planets
        print("\n🌍 SCENARIO 2: Casual Space Tourism")
        space_tour = [
            ("Start Tour", "yo lets do a tour of the planets"),
            ("Visit Earth", "first show me earth"),
            ("Check Moon", "whats the moon like from here"),
            ("Off to Venus", "venus looks bright lets go there"),
            ("Venus Photo", "capture this view"),
            ("Next Stop", "jupiter must be huge show me"),
            ("Saturn Rings", "saturn with those rings looks amazing"),
            ("Final Photo", "screenshot this please"),
        ]
        
        for test_name, command in space_tour:
            self.run_test(f"Space Tour - {test_name}", command)
            time.sleep(0.8)
        
        # Scenario 3: Quick commands rapid fire
        print("\n⚡ SCENARIO 3: Rapid Fire Commands")
        rapid_commands = [
            ("Quick Mars", "mars"),
            ("Quick Jupiter", "jupiter now"),
            ("Quick Photo", "pic"),
            ("Quick Moon", "moon"),
            ("Quick Help", "stuck"),
            ("Quick Saturn", "saturn rings"),
            ("Quick Back", "get me out"),
        ]
        
        for test_name, command in rapid_commands:
            self.run_test(f"Rapid Fire - {test_name}", command)
            time.sleep(0.2)  # Rapid fire - short delays
        
        # Scenario 4: Confused user getting help
        print("\n🤔 SCENARIO 4: Confused User Needs Help")
        confused_user = [
            ("Vague Request", "i want to see space stuff"),
            ("Try Again", "show me something cool"),
            ("More Specific", "maybe mars would be neat"),
            ("Success", "go to mars"),
            ("Another Try", "what else is there"),
            ("Jupiter Try", "that big planet jupiter"),
            ("Landing Try", "can i land somewhere"),
            ("Land on Moon", "land on the moon"),
            ("Photo Try", "save this somehow"),
            ("Photo Success", "take a screenshot"),
        ]
        
        for test_name, command in confused_user:
            self.run_test(f"Confused User - {test_name}", command)
            time.sleep(0.5)
        
        # Scenario 5: Power user advanced commands
        print("\n🧠 SCENARIO 5: Power User Advanced Usage")
        power_user = [
            ("Complex Tour", "cinematic journey to jupiter with landing"),
            ("Multi Step", "visit saturn then take a screenshot"),
            ("Stream Tour", "stream tour of the gas giants"),
            ("Technical Request", "go to mars and analyze atmosphere"),
            ("Recovery", "camera is stuck free it now"),
            ("Advanced Navigation", "navigate to alpha centauri smoothly"),
        ]
        
        for test_name, command in power_user:
            self.run_test(f"Power User - {test_name}", command)
            time.sleep(1.2)  # Longer delays for complex commands
    
    def run_quick_test(self) -> None:
        """Run essential tests only"""
        print("🚀 Running Quick Test Suite...")
        self.test_basic_navigation()
        self.test_camera_controls()
        
    def run_full_test(self) -> None:
        """Run comprehensive test suite"""
        print("🧪 Running Full Test Suite...")
        self.test_basic_navigation()
        self.test_landing_operations()
        self.test_tracking_operations()
        self.test_exploration_modes()
        self.test_camera_controls()
        self.test_complex_tours()
        self.test_multi_step_commands()
        self.test_error_scenarios()
        self.test_performance_timing()
        self.test_llm_vs_regex_fallback()
        self.test_natural_language_commands()
        self.test_realistic_simulation()
    
    def run_tool_test(self, tool_name: str) -> None:
        """Run tests for a specific tool"""
        print(f"🔧 Testing specific tool: {tool_name}")
        
        tool_commands = {
            "go_to": ["go to mars", "take me to jupiter"],
            "land_on": ["land on moon", "land on mars"],
            "track": ["track saturn", "follow jupiter"],
            "explore": ["explore venus", "investigate mars"],
            "screenshot": ["take screenshot", "capture image"],
            "tour": ["tour solar system", "tour planets"],
            "cinematic": ["cinematic journey to mars"],
            "stream": ["stream tour of jupiter"],
        }
        
        commands = tool_commands.get(tool_name, [f"test {tool_name}"])
        for command in commands:
            self.run_test(f"{tool_name.title()} Test", command)
            time.sleep(0.5)
    
    def generate_report(self) -> None:
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("📊 MASTER TEST SUITE REPORT")
        print("="*80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # Performance summary
        if self.results:
            avg_time = sum(r.execution_time for r in self.results) / len(self.results)
            max_time = max(r.execution_time for r in self.results)
            min_time = min(r.execution_time for r in self.results)
            
            print(f"\n⏱️ Performance Summary:")
            print(f"   Average Execution Time: {avg_time:.3f}s")
            print(f"   Fastest Command: {min_time:.3f}s")
            print(f"   Slowest Command: {max_time:.3f}s")
        
        # Failed tests details
        if failed_tests > 0:
            print(f"\n❌ Failed Tests Details:")
            for result in self.results:
                if not result.success:
                    print(f"   • {result.test_name}: {result.command}")
                    print(f"     Error: {result.error_details}")
                    print(f"     Output: {result.result_message[:100]}...")
        
        # Success summary
        print(f"\n🎯 System Health Score: {success_rate:.1f}%")
        if success_rate >= 90:
            print("   Status: 🟢 EXCELLENT - System working perfectly!")
        elif success_rate >= 75:
            print("   Status: 🟡 GOOD - Minor issues detected")
        elif success_rate >= 50:
            print("   Status: 🟠 NEEDS ATTENTION - Several issues found")
        else:
            print("   Status: 🔴 CRITICAL - Major problems detected")
        
        print("\n" + "="*80)
        
        # Save results to file
        self.save_results_to_file()
    
    def save_results_to_file(self, category: str = "unknown") -> None:
        """Save test results to a file for tracking"""
        import json
        from datetime import datetime
        
        results_file = "tests/test_results.json"
        
        # Load existing results
        try:
            with open(results_file, 'r') as f:
                all_results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_results = {}
        
        # Prepare current test data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine category from recent test names
        if self.results:
            first_test = self.results[0].test_name.lower()
            command_text = self.results[0].command.lower()
            
            # Check for multi-step first (higher priority)
            if 'multi' in first_test or 'then' in command_text or ' and ' in command_text:
                category = "multistep"
            elif any(land in first_test for land in ['land', 'touch down']):
                category = "landing"
            elif any(track in first_test for track in ['track', 'follow', 'watch']):
                category = "tracking"
            elif any(cam in first_test for cam in ['screenshot', 'camera', 'capture']):
                category = "camera"
            elif any(err in first_test for err in ['invalid', 'error', 'gibberish', 'empty']):
                category = "errors"
            elif any(tour in first_test for tour in ['tour', 'exploration', 'cinematic']):
                category = "tours"
            elif any(nav in first_test for nav in ['mars', 'jupiter', 'saturn', 'venus', 'go to']):
                category = "navigation"
            else:
                category = "general"
        
        # Initialize category if not exists
        if category not in all_results:
            all_results[category] = {
                "last_run": "",
                "total_runs": 0,
                "passed_tests": [],
                "failed_tests": []
            }
        
        # Update category data
        all_results[category]["last_run"] = timestamp
        all_results[category]["total_runs"] += 1
        
        # Clear previous results for this category and add current ones
        all_results[category]["passed_tests"] = []
        all_results[category]["failed_tests"] = []
        
        for result in self.results:
            test_data = {
                "command": result.command,
                "test_name": result.test_name,
                "execution_time": round(result.execution_time, 3),
                "timestamp": timestamp
            }
            
            if result.success:
                all_results[category]["passed_tests"].append(test_data)
            else:
                test_data["error"] = result.error_details or result.result_message
                all_results[category]["failed_tests"].append(test_data)
        
        # Save updated results
        try:
            with open(results_file, 'w') as f:
                json.dump(all_results, f, indent=2)
            print(f"💾 Results saved to {results_file}")
        except Exception as e:
            print(f"⚠️ Could not save results: {e}")

    def run_category_navigation(self) -> None:
        """Run only basic navigation tests"""
        print("🚀 TESTING BASIC NAVIGATION TOOLS")
        print("="*60)
        self.test_basic_navigation()

    def run_category_landing(self) -> None:
        """Run only landing operation tests"""
        print("🛬 TESTING LANDING OPERATIONS")
        print("="*60)
        self.test_landing_operations()

    def run_category_tracking(self) -> None:
        """Run only tracking tests"""
        print("👁️ TESTING TRACKING OPERATIONS")
        print("="*60)
        self.test_tracking_operations()

    def run_category_camera(self) -> None:
        """Run only camera control tests"""
        print("📷 TESTING CAMERA CONTROLS")
        print("="*60)
        self.test_camera_controls()

    def run_category_multistep(self) -> None:
        """Run only multi-step command tests"""
        print("🔄 TESTING MULTI-STEP COMMANDS")
        print("="*60)
        self.test_multi_step_commands()

    def run_category_errors(self) -> None:
        """Run only error scenario tests"""
        print("⚠️ TESTING ERROR SCENARIOS")
        print("="*60)
        self.test_error_scenarios()

    def run_category_tours(self) -> None:
        """Run tours and exploration tests"""
        print("🎬 TESTING COMPLEX TOURS & EXPLORATION")
        print("="*60)
        self.test_complex_tours()
        self.test_exploration_modes()

    def run_category_performance(self) -> None:
        """Run performance and timing tests"""
        print("⚡ TESTING PERFORMANCE & TIMING")
        print("="*60)
        self.test_performance_timing()

    def run_category_language(self) -> None:
        """Run natural language tests"""
        print("💬 TESTING NATURAL LANGUAGE")
        print("="*60)
        self.test_natural_language_commands()

    def run_interactive_mode(self) -> None:
        """Interactive mode for selective testing"""
        while True:
            print("\n" + "="*60)
            print("🚀 INTERACTIVE TEST MENU")
            print("="*60)
            print("1️⃣  Basic Navigation (go to planets)")
            print("2️⃣  Landing Operations (land on surfaces)")
            print("3️⃣  Tracking & Following (track objects)")
            print("4️⃣  Camera Controls (screenshot, free camera)")
            print("5️⃣  Multi-Step Commands (complex sequences)")
            print("6️⃣  Error Scenarios (invalid inputs)")
            print("7️⃣  Complex Tours & Exploration")
            print("8️⃣  Performance & Timing Tests")
            print("9️⃣  Natural Language Tests")
            print("🔟  Quick Test Suite (basic + camera)")
            print("🌟  Full Test Suite (everything)")
            print("❌  Quit")
            print("="*60)
            
            choice = input("Select category to test (1-10, full, quit): ").strip().lower()
            
            if choice in ['quit', 'q', 'exit']:
                print("👋 Thanks for testing! Goodbye!")
                break
            elif choice == '1':
                self.run_category_navigation()
            elif choice == '2':
                self.run_category_landing()
            elif choice == '3':
                self.run_category_tracking()
            elif choice == '4':
                self.run_category_camera()
            elif choice == '5':
                self.run_category_multistep()
            elif choice == '6':
                self.run_category_errors()
            elif choice == '7':
                self.run_category_tours()
            elif choice == '8':
                self.run_category_performance()
            elif choice == '9':
                self.run_category_language()
            elif choice == '10':
                print("\n🚀 Running Quick Test Suite...")
                self.run_quick_test()
            elif choice in ['full', 'f', 'all']:
                print("\n🌟 Running Full Test Suite...")
                self.run_full_test()
            else:
                print("❌ Invalid choice. Please try again.")
                continue
            
            # Show results after each test
            if self.results:
                self.generate_report()
                self.results = []  # Clear results for next test
            
            # Ask to continue
            print("\n" + "-"*40)
            continue_choice = input("Continue testing? (y/n): ").strip().lower()
            if continue_choice in ['n', 'no', 'quit']:
                print("👋 Thanks for testing! Goodbye!")
                break

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Master Test Suite for Remote Controller")
    parser.add_argument("--full", action="store_true", help="Run full comprehensive test suite")
    parser.add_argument("--quick", action="store_true", help="Run quick essential tests only")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run interactive mode with menu")
    parser.add_argument("--tool", type=str, help="Test specific tool (go_to, land_on, track, etc.)")
    parser.add_argument("--no-connection", action="store_true", help="Skip Gaia Sky connection test")
    
    # Category-specific tests
    parser.add_argument("--navigation", action="store_true", help="Test basic navigation only")
    parser.add_argument("--landing", action="store_true", help="Test landing operations only")
    parser.add_argument("--tracking", action="store_true", help="Test tracking operations only")
    parser.add_argument("--camera", action="store_true", help="Test camera controls only")
    parser.add_argument("--multistep", action="store_true", help="Test multi-step commands only")
    parser.add_argument("--errors", action="store_true", help="Test error scenarios only")
    parser.add_argument("--tours", action="store_true", help="Test tours and exploration only")
    parser.add_argument("--performance", action="store_true", help="Test performance and timing only")
    parser.add_argument("--language", action="store_true", help="Test natural language processing only")
    
    args = parser.parse_args()
    
    # Initialize test suite
    suite = MasterTestSuite()
    
    # Test connection unless skipped
    if not args.no_connection:
        if not suite.connect_to_gaia_sky():
            print("❌ Cannot proceed without Gaia Sky connection!")
            print("💡 Make sure Gaia Sky is running with Python bridge enabled")
            print("💡 Or use --no-connection to skip connection test")
            sys.exit(1)
    
    # Run appropriate test suite
    try:
        if args.interactive:
            suite.run_interactive_mode()
        elif args.navigation:
            suite.run_category_navigation()
        elif args.landing:
            suite.run_category_landing()
        elif args.tracking:
            suite.run_category_tracking()
        elif args.camera:
            suite.run_category_camera()
        elif args.multistep:
            suite.run_category_multistep()
        elif args.errors:
            suite.run_category_errors()
        elif args.tours:
            suite.run_category_tours()
        elif args.performance:
            suite.run_category_performance()
        elif args.language:
            suite.run_category_language()
        elif args.tool:
            suite.run_tool_test(args.tool)
        elif args.quick:
            suite.run_quick_test()
        elif args.full:
            suite.run_full_test()
        else:
            # Default: run interactive mode
            suite.run_interactive_mode()
        
        # Generate report (unless interactive mode handled it)
        if not args.interactive and suite.results:
            suite.generate_report()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Test suite interrupted by user")
        suite.generate_report()
    except Exception as e:
        print(f"\n\n💥 Test suite crashed: {e}")
        suite.generate_report()
        raise
    finally:
        # Cleanup
        suite.controller.disconnect()
        print("\n👋 Test suite completed!")


if __name__ == "__main__":
    main()