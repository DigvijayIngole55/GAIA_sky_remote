#!/usr/bin/env python3
"""
🗣️ CASUAL SPEECH PATTERN TEST
Tests very natural, conversational language as people actually speak
Focus on casual, human-like speech patterns instead of rigid commands
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from remote_controller import SimpleRemoteController

# Real casual speech patterns - how people actually talk
CASUAL_SPEECH_TESTS = [
    # Very casual, conversational
    "hey can we check out mars",
    "umm lets go see jupiter",
    "oh i wanna visit saturn", 
    "could we maybe go to venus",
    "yo take me to the moon",
    
    # With filler words and hesitation
    "so like can we go to mars or something",
    "uh i think i want to see jupiter",
    "well maybe we should visit saturn",
    "hmm lets check out venus i guess",
    "ok so um can we go to the moon",
    
    # Natural conversation flow
    "i'm curious about mars can we go there",
    "what does jupiter look like up close",
    "saturn must be beautiful with those rings",
    "venus is super hot right lets see it",
    "the moon looks cool tonight lets visit",
    
    # Casual requests with personality
    "dude take me to mars thats awesome",
    "oh wow jupiter is huge lets go there", 
    "saturn with the rings looks so cool",
    "venus sounds interesting lets check it out",
    "the moon is our neighbor lets visit",
    
    # Conversational with context
    "i heard mars is red can we see it",
    "jupiter has big storms right show me",
    "saturn has like crazy rings lets go",
    "venus is the hottest planet check it out",
    "the moon is so close lets go there",
    
    # Really casual/slang
    "mars looks sick lets go",
    "jupiter is massive show me that",
    "saturn is pretty af lets see it",
    "venus is hot as hell literally",
    "moon looks chill tonight",
    
    # Questions turned to requests
    "whats mars like up close",
    "how big is jupiter really",
    "are saturns rings actually that cool",
    "why is venus so bright",
    "what does earth look like from the moon",
    
    # Emotional/excited speech
    "oh my god mars would be so cool to see",
    "jupiter must be absolutely massive",
    "saturn is probably the prettiest planet",
    "venus looks so bright and mysterious", 
    "the moon is so peaceful and quiet",
    
    # Landing requests - very casual
    "can we actually land on the moon",
    "i wanna touch down on mars",
    "lets land on the moon and walk around",
    "put me down on mars surface",
    "drop me off on the moon",
    
    # Photo requests - natural
    "this looks amazing take a picture",
    "get a photo of this view",
    "save this its so beautiful", 
    "capture this moment",
    "screenshot this please",
    
    # Recovery - frustrated/stuck
    "help im stuck here",
    "get me out of this mess",
    "something went wrong fix it",
    "the view is all weird",
    "camera is acting up",
    "i cant move properly",
    
    # Complex natural requests
    "take me to mars and let me walk around",
    "i want to see jupiter then take a picture",
    "show me saturn up close and personal",
    "venus tour would be awesome",
    "moon trip with landing please",
    
    # Questions that imply commands
    "what would mars look like from orbit",
    "how close can we get to jupiter",
    "can i see saturn rings from nearby",
    "what happens if we land on the moon",
    "is venus surface visible through clouds",
    
    # Stream of consciousness
    "so like mars is the red planet right and i really wanna see what it looks like",
    "jupiter is this massive gas giant and i bet the view is incredible",
    "saturn has those crazy beautiful rings that must be amazing to see",
    "venus is like super hot and bright so that would be interesting",
    "the moon is right there and we should totally check it out",
    
    # Enthusiastic/young speech
    "mars is so cool can we go please please",
    "jupiter is like the biggest thing ever",
    "saturn is literally the prettiest planet",
    "venus is like a hot mess but cool",
    "moon adventure time lets go",
    
    # Tired/casual evening speech
    "eh lets just go to mars i guess",
    "whatever jupiter sounds fine",
    "sure saturn why not",
    "venus ok cool",
    "moon whatever",
    
    # Comparative speech
    "mars is cooler than earth lets go",
    "jupiter is way bigger than anything",
    "saturn beats all other planets",
    "venus is hotter than mars even",
    "moon is smaller but closer",
    
    # Storytelling style
    "so theres this planet called mars",
    "you know jupiter the big one",
    "saturn the one with rings",
    "venus the morning star",
    "our moon up there",
    
    # Mixed with other topics
    "after dinner can we visit mars",
    "before bed lets see the moon",
    "its friday lets party on jupiter",
    "weekend trip to saturn sounds good",
    "monday morning venus visit",
    
    # Regional/dialectal variations
    "reckon we could mosey on over to mars",
    "fancy a trip to jupiter mate",
    "how bout we cruise to saturn",
    "lets mosey on down to venus",
    "wanna pop over to the moon",
    
    # Technical but casual
    "mars has that thin atmosphere right",
    "jupiter with the great red spot", 
    "saturn and those icy rings",
    "venus with the thick clouds",
    "moon with the low gravity"
]

def test_casual_speech():
    """Test natural, casual speech patterns"""
    
    print("🗣️ CASUAL SPEECH PATTERN TEST")
    print("🎯 Testing natural conversational language")
    print("=" * 60)
    
    controller = SimpleRemoteController()
    
    results = []
    
    for i, speech in enumerate(CASUAL_SPEECH_TESTS, 1):
        print(f"\n[{i:2}/{len(CASUAL_SPEECH_TESTS)}] Testing casual speech:")
        print(f"🎤 Input: '{speech}'")
        
        try:
            # Execute the natural language command
            result = controller.execute_command(speech)
            
            # Determine success
            success = not result.startswith("❌") and not result.startswith("Sorry")
            status = "✅" if success else "❌"
            
            print(f"{status} Output: {result}")
            
            results.append({
                "input": speech,
                "output": result, 
                "success": success
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "input": speech,
                "output": f"Exception: {e}",
                "success": False
            })
        
        time.sleep(0.1)  # Small delay
    
    # Calculate statistics
    total_tests = len(results)
    successful = sum(1 for r in results if r["success"])
    success_rate = (successful / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n" + "=" * 60)
    print(f"📊 CASUAL SPEECH TEST RESULTS")
    print(f"=" * 60)
    print(f"🧪 Total Casual Phrases: {total_tests}")
    print(f"✅ Successfully Understood: {successful}")
    print(f"❌ Failed to Understand: {total_tests - successful}")
    print(f"📈 Natural Language Success Rate: {success_rate:.1f}%")
    
    # Show some examples of successes and failures
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]
    
    if successes:
        print(f"\n✅ EXAMPLES OF UNDERSTOOD SPEECH:")
        for example in successes[:5]:
            print(f"  🎤 '{example['input']}'")
            print(f"  🤖 '{example['output']}'")
            print()
    
    if failures:
        print(f"\n❌ EXAMPLES OF MISUNDERSTOOD SPEECH:")
        for example in failures[:5]:
            print(f"  🎤 '{example['input']}'")
            print(f"  🤖 '{example['output']}'")
            print()
    
    # Provide feedback
    if success_rate >= 80:
        print("🎉 EXCELLENT! The system handles very natural speech really well!")
        print("🗣️ People can talk normally and casually")
    elif success_rate >= 60:
        print("👍 GOOD! The system understands most casual speech")
        print("🗣️ Some improvement needed for very casual language")
    elif success_rate >= 40:
        print("⚠️ MODERATE! The system struggles with casual speech")
        print("🗣️ Users need to speak more formally")
    else:
        print("🚨 POOR! The system doesn't handle natural speech well")
        print("🗣️ Users must use very specific commands")
    
    return results

if __name__ == "__main__":
    test_casual_speech()