#!/usr/bin/env python3
"""
🎯 REAL SPEECH PATTERNS TEST
Super simple test with the most challenging natural language
Tests how people ACTUALLY talk when using voice commands
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from remote_controller import SimpleRemoteController

# How people ACTUALLY talk - messy, natural, real speech
REAL_SPEECH_EXAMPLES = [
    # Super casual everyday speech
    "yo lets check out mars",
    "umm can we go to jupiter", 
    "oh saturn looks cool",
    "hey show me venus",
    "dude take me to the moon",
    
    # Questions that mean commands
    "whats mars like",
    "how big is jupiter",
    "what do saturn rings look like",
    "is venus really that hot",
    "can we see earth from the moon",
    
    # Hesitant/uncertain speech
    "maybe we could go to mars",
    "i think jupiter would be cool",
    "saturn might be interesting", 
    "venus could be worth seeing",
    "the moon seems nice",
    
    # Excited/emotional
    "mars is so awesome",
    "jupiter must be incredible", 
    "saturn is beautiful",
    "venus looks mysterious",
    "the moon is amazing",
    
    # Mumbled/unclear (as speech recognition might hear)
    "go ta mars",
    "take me ta jupiter",
    "show me satrun", 
    "venus plz",
    "moon trip",
    
    # With filler words
    "like go to mars",
    "you know jupiter",
    "so um saturn",
    "well venus",
    "uh the moon",
    
    # Really casual slang
    "mars looks sick",
    "jupiter is mental",
    "saturn is lit", 
    "venus is fire",
    "moon vibes",
    
    # Photo requests - natural
    "this is cool take a pic",
    "get a photo",
    "save this view",
    "screenshot plz",
    
    # When stuck/frustrated  
    "help im stuck",
    "get me out",
    "this is broken",
    "cant move",
    
    # Complex but natural
    "take me to mars and land there",
    "jupiter close up would be cool",
    "saturn tour sounds awesome"
]

def quick_speech_test():
    """Quick test of real speech patterns"""
    
    print("🎯 REAL SPEECH PATTERNS TEST")
    print("🗣️ Testing how people actually talk")
    print("=" * 50)
    
    controller = SimpleRemoteController()
    
    passed = 0
    total = len(REAL_SPEECH_EXAMPLES)
    
    for i, speech in enumerate(REAL_SPEECH_EXAMPLES, 1):
        print(f"\n[{i:2}] 🎤 '{speech}'")
        
        try:
            result = controller.execute_command(speech)
            
            # Check if it understood (not an error message)
            if not result.startswith("❌") and not result.startswith("Sorry"):
                print(f"    ✅ {result}")
                passed += 1
            else:
                print(f"    ❌ {result}")
                
        except Exception as e:
            print(f"    💥 Error: {e}")
    
    # Quick summary
    success_rate = (passed / total * 100)
    print(f"\n" + "=" * 50)
    print(f"📊 RESULTS: {passed}/{total} ({success_rate:.0f}%)")
    
    if success_rate >= 70:
        print("🎉 GREAT! Handles real speech well!")
    elif success_rate >= 50:
        print("👍 GOOD! Most real speech works!")
    else:
        print("⚠️ NEEDS WORK! Struggles with real speech!")

if __name__ == "__main__":
    quick_speech_test()