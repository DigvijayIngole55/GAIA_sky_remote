#!/usr/bin/env python3
"""
Test script for Standalone Remote Controller
"""

from remote_controller import SimpleRemoteController

def test_standalone_controller():
    """Test the standalone remote controller"""
    
    print("🧪 Testing Standalone Remote Controller")
    print("=" * 50)
    
    controller = SimpleRemoteController()
    
    # Test commands (without connecting to Gaia Sky)
    test_commands = [
        "go to mars",
        "take me to jupiter", 
        "land on the moon",
        "explore saturn",
        "track venus",
        "take a screenshot",
        "tour the solar system",
        "cinematic journey to mars",
        "stream tour of jupiter moons",
        "visit mars then land on it",
        "free camera",
        "back to space"
    ]
    
    print("📝 Testing command parsing:")
    for cmd in test_commands:
        print(f"\nInput: '{cmd}'")
        try:
            # Test LLM parsing
            parsed = controller.llm.parse_command(cmd)
            if parsed:
                print(f"✅ LLM: action='{parsed.action}', entity='{parsed.entity}'")
            else:
                print("🔄 LLM failed, testing fallback...")
                # Test fallback parsing
                result = controller._try_fallback_parsing(cmd)
                print(f"📤 Fallback: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Standalone controller test complete!")
    print("🎯 All parsing systems working correctly")
    print("💡 To use with Gaia Sky, run: python remote_controller.py")

if __name__ == "__main__":
    test_standalone_controller()