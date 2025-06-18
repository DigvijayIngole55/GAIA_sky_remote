#!/usr/bin/env python3
"""
🎤 DIRECT NATURAL LANGUAGE COMMAND EXECUTION TEST
Tests natural language commands by directly triggering remote controller execution
Bypasses LLM parsing and simulates real speech-to-controller flow
"""

import sys
import os
import time
from typing import Dict, List

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from remote_controller import SimpleRemoteController
from natural_language_test_cases import *

class DirectCommandTester:
    """Test natural language commands by directly executing them through the controller"""
    
    def __init__(self):
        self.controller = SimpleRemoteController()
        self.test_results = []
        
    def execute_command_test(self, command_text: str, category: str = "") -> Dict:
        """
        Execute a command directly through the controller and capture results
        
        Args:
            command_text: Natural language command to execute
            category: Test category for organization
            
        Returns:
            Dict with test results
        """
        print(f"🎤 Testing: '{command_text}'")
        
        start_time = time.time()
        
        try:
            # Execute command directly through controller (like speech would)
            result = self.controller.execute_command(command_text)
            execution_time = time.time() - start_time
            
            # Determine if execution was successful based on result
            success = not result.startswith("❌") and not result.startswith("Sorry")
            
            test_result = {
                "input": command_text,
                "category": category,
                "output": result,
                "success": success,
                "execution_time": execution_time,
                "timestamp": time.time()
            }
            
            # Print immediate feedback
            status = "✅" if success else "❌"
            print(f"  {status} Result: {result}")
            print(f"  ⏱️ Time: {execution_time:.3f}s")
            
            self.test_results.append(test_result)
            return test_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            test_result = {
                "input": command_text,
                "category": category,
                "output": f"Exception: {str(e)}",
                "success": False,
                "execution_time": execution_time,
                "timestamp": time.time()
            }
            
            print(f"  ❌ Exception: {str(e)}")
            print(f"  ⏱️ Time: {execution_time:.3f}s")
            
            self.test_results.append(test_result)
            return test_result
    
    def test_navigation_commands(self):
        """Test all navigation command variations"""
        print("🚀 TESTING NAVIGATION COMMANDS")
        print("=" * 60)
        
        for entity, commands in NAVIGATION_TEST_CASES.items():
            print(f"\n📍 Testing {entity.upper()} navigation ({len(commands)} variants)")
            
            for i, command in enumerate(commands[:5], 1):  # Test first 5 of each entity
                print(f"\n[{i}/5] {entity.upper()}:")
                self.execute_command_test(command, f"navigation_{entity}")
                time.sleep(0.1)  # Small delay between commands
    
    def test_landing_commands(self):
        """Test all landing command variations"""
        print("\n🛬 TESTING LANDING COMMANDS")
        print("=" * 60)
        
        for entity, commands in LANDING_TEST_CASES.items():
            print(f"\n🎯 Testing {entity.upper()} landing ({len(commands)} variants)")
            
            for i, command in enumerate(commands, 1):
                print(f"\n[{i}/{len(commands)}] {entity.upper()}:")
                self.execute_command_test(command, f"landing_{entity}")
                time.sleep(0.1)
    
    def test_tracking_commands(self):
        """Test all tracking command variations"""
        print("\n👁️ TESTING TRACKING COMMANDS")
        print("=" * 60)
        
        for entity, commands in TRACKING_TEST_CASES.items():
            print(f"\n🔍 Testing {entity.upper()} tracking ({len(commands)} variants)")
            
            for i, command in enumerate(commands, 1):
                print(f"\n[{i}/{len(commands)}] {entity.upper()}:")
                self.execute_command_test(command, f"tracking_{entity}")
                time.sleep(0.1)
    
    def test_exploration_commands(self):
        """Test all exploration command variations"""
        print("\n🔍 TESTING EXPLORATION COMMANDS")
        print("=" * 60)
        
        for entity, commands in EXPLORATION_TEST_CASES.items():
            print(f"\n🌌 Testing {entity.upper()} exploration ({len(commands)} variants)")
            
            for i, command in enumerate(commands, 1):
                print(f"\n[{i}/{len(commands)}] {entity.upper()}:")
                self.execute_command_test(command, f"exploration_{entity}")
                time.sleep(0.1)
    
    def test_photography_commands(self):
        """Test all photography command variations"""
        print("\n📸 TESTING PHOTOGRAPHY COMMANDS")
        print("=" * 60)
        
        for i, command in enumerate(PHOTOGRAPHY_TEST_CASES, 1):
            print(f"\n[{i}/{len(PHOTOGRAPHY_TEST_CASES)}] SCREENSHOT:")
            self.execute_command_test(command, "photography")
            time.sleep(0.1)
    
    def test_recovery_commands(self):
        """Test all recovery command variations"""
        print("\n🆘 TESTING RECOVERY COMMANDS")
        print("=" * 60)
        
        for action, commands in RECOVERY_TEST_CASES.items():
            print(f"\n🔧 Testing {action.upper()} ({len(commands)} variants)")
            
            for i, command in enumerate(commands, 1):
                print(f"\n[{i}/{len(commands)}] {action.upper()}:")
                self.execute_command_test(command, f"recovery_{action}")
                time.sleep(0.1)
    
    def test_multi_tool_commands(self):
        """Test multi-tool command variations"""
        print("\n🎬 TESTING MULTI-TOOL COMMANDS")
        print("=" * 60)
        
        # Test tour commands
        print("\n🗺️ TOUR COMMANDS:")
        for tour_type, commands in TOUR_TEST_CASES.items():
            print(f"\n🎯 Testing {tour_type.upper()} tours ({len(commands)} variants)")
            
            for i, command in enumerate(commands, 1):
                print(f"\n[{i}/{len(commands)}] {tour_type.upper()}:")
                self.execute_command_test(command, f"tour_{tour_type}")
                time.sleep(0.2)  # Longer delay for complex commands
        
        # Test cinematic commands
        print("\n🎥 CINEMATIC COMMANDS:")
        for entity, commands in CINEMATIC_TEST_CASES.items():
            print(f"\n🎬 Testing {entity.upper()} cinematic ({len(commands)} variants)")
            
            for i, command in enumerate(commands, 1):
                print(f"\n[{i}/{len(commands)}] {entity.upper()}:")
                self.execute_command_test(command, f"cinematic_{entity}")
                time.sleep(0.2)
        
        # Test stream tour commands
        print("\n📺 STREAM TOUR COMMANDS:")
        for entity, commands in STREAM_TOUR_TEST_CASES.items():
            print(f"\n🎥 Testing {entity.upper()} stream tours ({len(commands)} variants)")
            
            for i, command in enumerate(commands, 1):
                print(f"\n[{i}/{len(commands)}] {entity.upper()}:")
                self.execute_command_test(command, f"stream_{entity}")
                time.sleep(0.2)
        
        # Test multi-step commands
        print("\n🔄 MULTI-STEP COMMANDS:")
        for i, command in enumerate(MULTI_STEP_TEST_CASES, 1):
            print(f"\n[{i}/{len(MULTI_STEP_TEST_CASES)}] MULTI-STEP:")
            self.execute_command_test(command, "multi_step")
            time.sleep(0.3)  # Longest delay for complex sequences
    
    def test_conversational_commands(self):
        """Test conversational command patterns"""
        print("\n💬 TESTING CONVERSATIONAL COMMANDS")
        print("=" * 60)
        
        for i, command in enumerate(CONVERSATIONAL_TEST_CASES, 1):
            print(f"\n[{i}/{len(CONVERSATIONAL_TEST_CASES)}] CONVERSATIONAL:")
            self.execute_command_test(command, "conversational")
            time.sleep(0.1)
    
    def test_difficult_cases(self):
        """Test difficult/edge case commands"""
        print("\n⚠️ TESTING DIFFICULT CASES")
        print("=" * 60)
        
        for i, command in enumerate(DIFFICULT_TEST_CASES, 1):
            print(f"\n[{i}/{len(DIFFICULT_TEST_CASES)}] DIFFICULT:")
            self.execute_command_test(command, "difficult")
            time.sleep(0.1)
    
    def run_comprehensive_test_suite(self):
        """Run all test categories"""
        print("🧪 COMPREHENSIVE NATURAL LANGUAGE COMMAND TEST SUITE")
        print("🎤 Simulating direct speech-to-controller execution")
        print("=" * 80)
        
        start_time = time.time()
        
        # Run all test categories
        self.test_navigation_commands()
        self.test_landing_commands()
        self.test_tracking_commands()
        self.test_exploration_commands()
        self.test_photography_commands()
        self.test_recovery_commands()
        self.test_multi_tool_commands()
        self.test_conversational_commands()
        self.test_difficult_cases()
        
        total_time = time.time() - start_time
        
        # Calculate statistics
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        avg_execution_time = sum(r["execution_time"] for r in self.test_results) / total_tests if total_tests > 0 else 0
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 80)
        print(f"🧪 Total Commands Tested: {total_tests}")
        print(f"✅ Successful Executions: {successful_tests}")
        print(f"❌ Failed Executions: {failed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"⏱️ Average Execution Time: {avg_execution_time:.3f}s")
        print(f"🕐 Total Test Duration: {total_time:.1f}s")
        
        # Show category breakdown
        print(f"\n📋 RESULTS BY CATEGORY:")
        categories = {}
        for result in self.test_results:
            category = result["category"]
            if category not in categories:
                categories[category] = {"total": 0, "successful": 0}
            categories[category]["total"] += 1
            if result["success"]:
                categories[category]["successful"] += 1
        
        for category, stats in sorted(categories.items()):
            success_rate = (stats["successful"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"  {category:25} {stats['successful']:3}/{stats['total']:3} ({success_rate:5.1f}%)")
        
        # Show failed commands
        failed_commands = [r for r in self.test_results if not r["success"]]
        if failed_commands:
            print(f"\n❌ FAILED COMMANDS ({len(failed_commands)} total):")
            for i, failure in enumerate(failed_commands[:10], 1):  # Show first 10 failures
                print(f"  {i:2}. '{failure['input']}'")
                print(f"      → {failure['output']}")
            
            if len(failed_commands) > 10:
                print(f"      ... and {len(failed_commands) - 10} more failures")
        
        print("\n" + "=" * 80)
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "avg_execution_time": avg_execution_time,
            "total_time": total_time,
            "results": self.test_results
        }

def main():
    """Main test execution function"""
    print("🎤 DIRECT NATURAL LANGUAGE COMMAND TESTING")
    print("🎯 Executing commands directly through RemoteController")
    print("⚠️ Note: This test does NOT connect to Gaia Sky - it tests command processing only")
    print()
    
    tester = DirectCommandTester()
    
    try:
        # Run comprehensive test suite
        results = tester.run_comprehensive_test_suite()
        
        # Save results to file
        import json
        output_file = "direct_natural_language_test_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Detailed results saved to: {output_file}")
        
        if results["success_rate"] >= 90:
            print("🎉 EXCELLENT! Natural language processing is working very well!")
        elif results["success_rate"] >= 75:
            print("👍 GOOD! Natural language processing is working well with some areas for improvement.")
        elif results["success_rate"] >= 50:
            print("⚠️ MODERATE! Natural language processing needs improvement.")
        else:
            print("🚨 POOR! Natural language processing needs significant improvement.")
        
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        raise

if __name__ == "__main__":
    main()