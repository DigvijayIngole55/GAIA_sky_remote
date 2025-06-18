#!/usr/bin/env python3
"""
🧪 NATURAL LANGUAGE PARSER TESTING SUITE
Automated testing for speech command recognition and parsing
Tests LLM parsing accuracy with extensive natural language variations
"""

import sys
import os
import json
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from remote_controller import SimpleLLMProvider, Command
from natural_language_test_cases import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Test result structure"""
    input_text: str
    expected_action: str
    expected_entity: str
    parsed_command: Optional[Command]
    success: bool
    error_message: str = ""
    execution_time: float = 0.0

class NaturalLanguageTestSuite:
    """
    Comprehensive test suite for natural language command parsing
    """
    
    def __init__(self):
        self.llm_provider = SimpleLLMProvider()
        self.test_results: List[TestResult] = []
        
    def test_command_parsing(self, text: str, expected_action: str, expected_entity: str = "") -> TestResult:
        """
        Test individual command parsing
        
        Args:
            text: Natural language input
            expected_action: Expected action to be parsed
            expected_entity: Expected entity to be parsed
            
        Returns:
            TestResult with parsing results
        """
        start_time = time.time()
        
        try:
            # Parse command using LLM
            parsed_command = self.llm_provider.parse_command(text)
            execution_time = time.time() - start_time
            
            if not parsed_command:
                return TestResult(
                    input_text=text,
                    expected_action=expected_action,
                    expected_entity=expected_entity,
                    parsed_command=None,
                    success=False,
                    error_message="Failed to parse command",
                    execution_time=execution_time
                )
            
            # Check if parsing matches expectations
            action_match = parsed_command.action.lower() == expected_action.lower()
            
            # For entity matching, be flexible with case and common variations
            entity_match = True
            if expected_entity:
                parsed_entity = parsed_command.entity.lower().strip()
                expected_entity_lower = expected_entity.lower().strip()
                
                # Direct match
                if parsed_entity == expected_entity_lower:
                    entity_match = True
                # Check common aliases
                elif self._check_entity_aliases(parsed_entity, expected_entity_lower):
                    entity_match = True
                else:
                    entity_match = False
            
            success = action_match and entity_match
            error_msg = ""
            
            if not action_match:
                error_msg += f"Action mismatch: expected '{expected_action}', got '{parsed_command.action}'. "
            if not entity_match:
                error_msg += f"Entity mismatch: expected '{expected_entity}', got '{parsed_command.entity}'. "
            
            return TestResult(
                input_text=text,
                expected_action=expected_action,
                expected_entity=expected_entity,
                parsed_command=parsed_command,
                success=success,
                error_message=error_msg.strip(),
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                input_text=text,
                expected_action=expected_action,
                expected_entity=expected_entity,
                parsed_command=None,
                success=False,
                error_message=f"Exception during parsing: {str(e)}",
                execution_time=execution_time
            )
    
    def _check_entity_aliases(self, parsed: str, expected: str) -> bool:
        """Check if parsed entity matches expected through common aliases"""
        aliases = {
            "mars": ["red planet", "fourth planet"],
            "earth": ["blue planet", "home", "our planet"],
            "moon": ["luna", "earth's moon"],
            "jupiter": ["gas giant", "largest planet", "jove"],
            "saturn": ["ringed planet", "ring planet"],
            "sun": ["our star", "sol", "solar center"],
            "venus": ["morning star", "evening star", "hottest planet"],
            "mercury": ["innermost planet", "fastest planet"],
            "neptune": ["ice giant", "blue planet", "windy planet"],
            "uranus": ["tilted planet", "sideways planet", "ice giant"],
            "pluto": ["dwarf planet", "distant world"],
            "iss": ["international space station", "space station"],
            "hubble": ["hubble telescope", "hubble space telescope"]
        }
        
        # Check if parsed entity is an alias for expected entity
        for entity, entity_aliases in aliases.items():
            if expected == entity and parsed in entity_aliases:
                return True
            if parsed == entity and expected in entity_aliases:
                return True
                
        return False
    
    def run_navigation_tests(self) -> Dict[str, List[TestResult]]:
        """Run all navigation command tests"""
        print("🚀 Testing Navigation Commands...")
        results = {}
        
        for entity, test_cases in NAVIGATION_TEST_CASES.items():
            print(f"  Testing {entity.upper()} navigation ({len(test_cases)} cases)")
            entity_results = []
            
            for test_case in test_cases:
                result = self.test_command_parsing(test_case, "go_to", entity)
                entity_results.append(result)
                
            results[f"nav_{entity}"] = entity_results
            success_rate = sum(1 for r in entity_results if r.success) / len(entity_results) * 100
            print(f"    ✅ Success rate: {success_rate:.1f}%")
            
        return results
    
    def run_landing_tests(self) -> Dict[str, List[TestResult]]:
        """Run all landing command tests"""
        print("🛬 Testing Landing Commands...")
        results = {}
        
        for entity, test_cases in LANDING_TEST_CASES.items():
            print(f"  Testing {entity.upper()} landing ({len(test_cases)} cases)")
            entity_results = []
            
            for test_case in test_cases:
                result = self.test_command_parsing(test_case, "land_on", entity)
                entity_results.append(result)
                
            results[f"land_{entity}"] = entity_results
            success_rate = sum(1 for r in entity_results if r.success) / len(entity_results) * 100
            print(f"    ✅ Success rate: {success_rate:.1f}%")
            
        return results
    
    def run_tracking_tests(self) -> Dict[str, List[TestResult]]:
        """Run all tracking command tests"""
        print("👁️ Testing Tracking Commands...")
        results = {}
        
        for entity, test_cases in TRACKING_TEST_CASES.items():
            print(f"  Testing {entity.upper()} tracking ({len(test_cases)} cases)")
            entity_results = []
            
            for test_case in test_cases:
                result = self.test_command_parsing(test_case, "track", entity)
                entity_results.append(result)
                
            results[f"track_{entity}"] = entity_results
            success_rate = sum(1 for r in entity_results if r.success) / len(entity_results) * 100
            print(f"    ✅ Success rate: {success_rate:.1f}%")
            
        return results
    
    def run_exploration_tests(self) -> Dict[str, List[TestResult]]:
        """Run all exploration command tests"""
        print("🔍 Testing Exploration Commands...")
        results = {}
        
        for entity, test_cases in EXPLORATION_TEST_CASES.items():
            print(f"  Testing {entity.upper()} exploration ({len(test_cases)} cases)")
            entity_results = []
            
            for test_case in test_cases:
                result = self.test_command_parsing(test_case, "explore", entity)
                entity_results.append(result)
                
            results[f"explore_{entity}"] = entity_results
            success_rate = sum(1 for r in entity_results if r.success) / len(entity_results) * 100
            print(f"    ✅ Success rate: {success_rate:.1f}%")
            
        return results
    
    def run_photography_tests(self) -> List[TestResult]:
        """Run all photography command tests"""
        print("📸 Testing Photography Commands...")
        results = []
        
        for test_case in PHOTOGRAPHY_TEST_CASES:
            result = self.test_command_parsing(test_case, "take_screenshot", "")
            results.append(result)
            
        success_rate = sum(1 for r in results if r.success) / len(results) * 100
        print(f"  ✅ Success rate: {success_rate:.1f}%")
        
        return results
    
    def run_recovery_tests(self) -> Dict[str, List[TestResult]]:
        """Run all recovery command tests"""
        print("🆘 Testing Recovery Commands...")
        results = {}
        
        for action, test_cases in RECOVERY_TEST_CASES.items():
            print(f"  Testing {action.upper()} ({len(test_cases)} cases)")
            action_results = []
            
            for test_case in test_cases:
                result = self.test_command_parsing(test_case, action, "")
                action_results.append(result)
                
            results[action] = action_results
            success_rate = sum(1 for r in action_results if r.success) / len(action_results) * 100
            print(f"    ✅ Success rate: {success_rate:.1f}%")
            
        return results
    
    def run_conversational_tests(self) -> List[TestResult]:
        """Run conversational pattern tests"""
        print("💬 Testing Conversational Patterns...")
        results = []
        
        # These are more complex - try to extract intent
        for test_case in CONVERSATIONAL_TEST_CASES:
            # For conversational tests, we'll be more lenient about the action
            # as long as the entity is correctly identified
            if "mars" in test_case.lower():
                expected_entity = "mars"
            elif "jupiter" in test_case.lower():
                expected_entity = "jupiter"
            elif "saturn" in test_case.lower():
                expected_entity = "saturn"
            elif "venus" in test_case.lower():
                expected_entity = "venus"
            else:
                expected_entity = ""
                
            result = self.test_command_parsing(test_case, "go_to", expected_entity)
            results.append(result)
            
        success_rate = sum(1 for r in results if r.success) / len(results) * 100
        print(f"  ✅ Success rate: {success_rate:.1f}%")
        
        return results
    
    def run_full_test_suite(self) -> Dict:
        """Run complete test suite"""
        print("🧪 NATURAL LANGUAGE PARSER TEST SUITE")
        print("=" * 60)
        
        all_results = {}
        start_time = time.time()
        
        # Run all test categories
        all_results.update(self.run_navigation_tests())
        all_results.update(self.run_landing_tests())
        all_results.update(self.run_tracking_tests())
        all_results.update(self.run_exploration_tests())
        all_results["photography"] = self.run_photography_tests()
        all_results.update(self.run_recovery_tests())
        all_results["conversational"] = self.run_conversational_tests()
        
        total_time = time.time() - start_time
        
        # Calculate overall statistics
        all_test_results = []
        for category, results in all_results.items():
            if isinstance(results, list):
                all_test_results.extend(results)
            else:
                for sub_results in results.values():
                    all_test_results.extend(sub_results)
        
        total_tests = len(all_test_results)
        successful_tests = sum(1 for r in all_test_results if r.success)
        overall_success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        avg_execution_time = sum(r.execution_time for r in all_test_results) / total_tests if total_tests > 0 else 0
        
        print(f"\n📊 OVERALL RESULTS")
        print(f"=" * 30)
        print(f"Total tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success rate: {overall_success_rate:.1f}%")
        print(f"Average execution time: {avg_execution_time:.3f}s")
        print(f"Total execution time: {total_time:.1f}s")
        
        return {
            "results": all_results,
            "statistics": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": total_tests - successful_tests,
                "success_rate": overall_success_rate,
                "avg_execution_time": avg_execution_time,
                "total_execution_time": total_time
            }
        }
    
    def generate_failure_report(self, results: Dict) -> str:
        """Generate detailed failure report"""
        report = []
        report.append("🚨 FAILURE ANALYSIS REPORT")
        report.append("=" * 50)
        
        for category, category_results in results["results"].items():
            if isinstance(category_results, list):
                failures = [r for r in category_results if not r.success]
            else:
                failures = []
                for sub_results in category_results.values():
                    failures.extend([r for r in sub_results if not r.success])
            
            if failures:
                report.append(f"\n❌ {category.upper()} FAILURES:")
                for failure in failures[:5]:  # Show first 5 failures
                    report.append(f"  Input: '{failure.input_text}'")
                    report.append(f"  Expected: {failure.expected_action} {failure.expected_entity}")
                    if failure.parsed_command:
                        report.append(f"  Got: {failure.parsed_command.action} {failure.parsed_command.entity}")
                    report.append(f"  Error: {failure.error_message}")
                    report.append("")
                
                if len(failures) > 5:
                    report.append(f"  ... and {len(failures) - 5} more failures")
        
        return "\n".join(report)

def main():
    """Main test execution"""
    test_suite = NaturalLanguageTestSuite()
    
    try:
        # Run full test suite
        results = test_suite.run_full_test_suite()
        
        # Generate failure report if there are failures
        if results["statistics"]["failed_tests"] > 0:
            failure_report = test_suite.generate_failure_report(results)
            print(f"\n{failure_report}")
        
        # Save results to file
        output_file = "natural_language_test_results.json"
        with open(output_file, 'w') as f:
            # Convert TestResult objects to dictionaries for JSON serialization
            json_results = {}
            for category, category_results in results["results"].items():
                if isinstance(category_results, list):
                    json_results[category] = [
                        {
                            "input_text": r.input_text,
                            "expected_action": r.expected_action,
                            "expected_entity": r.expected_entity,
                            "parsed_action": r.parsed_command.action if r.parsed_command else None,
                            "parsed_entity": r.parsed_command.entity if r.parsed_command else None,
                            "success": r.success,
                            "error_message": r.error_message,
                            "execution_time": r.execution_time
                        }
                        for r in category_results
                    ]
            
            json.dump({
                "test_results": json_results,
                "statistics": results["statistics"]
            }, f, indent=2)
        
        print(f"\n💾 Results saved to {output_file}")
        
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        raise

if __name__ == "__main__":
    main()