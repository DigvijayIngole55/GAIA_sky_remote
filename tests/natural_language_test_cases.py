#!/usr/bin/env python3
"""
🎤 EXTENSIVE NATURAL LANGUAGE TEST CASES
Comprehensive speech variations for testing voice command recognition
Real-world speech patterns, colloquialisms, and pronunciation variations
"""

# ==================== NAVIGATION COMMANDS ====================

NAVIGATION_TEST_CASES = {
    # MARS - The Red Planet
    "mars": [
        # Formal variations
        "go to mars", "take me to mars", "navigate to mars", "travel to mars",
        "fly to mars", "head to mars", "bring me to mars", "show me mars",
        
        # Casual/colloquial
        "let's go to mars", "can we go to mars", "i want to go to mars",
        "take us to mars", "mars please", "off to mars", "mars now",
        
        # With articles/prepositions
        "go to the mars", "take me to the red planet", "visit mars",
        "find mars", "locate mars", "get to mars",
        
        # Pronunciation variations (as they might be transcribed)
        "go to mars", "take me two mars", "go too mars", "mars pls",
        
        # Descriptive references
        "go to the red planet", "take me to the red planet",
        "navigate to the fourth planet", "visit the rusty planet",
        
        # Speed/urgency variations
        "quickly go to mars", "fast travel to mars", "immediately go to mars",
        "slowly navigate to mars", "carefully go to mars"
    ],
    
    # EARTH - Home Planet
    "earth": [
        "go to earth", "take me to earth", "return to earth", "back to earth",
        "go home", "take me home", "return home", "back home",
        "go to the earth", "take me to the blue planet", "visit earth",
        "navigate to earth", "travel to earth", "head to earth",
        "show me earth", "find earth", "locate earth",
        "go to our planet", "take me to our world", "return to our planet",
        "earth please", "home please", "get me home",
        "go back to earth", "return to the blue marble"
    ],
    
    # MOON - Earth's Satellite
    "moon": [
        "go to the moon", "take me to the moon", "navigate to the moon",
        "travel to the moon", "fly to the moon", "visit the moon",
        "go to moon", "take me to moon", "show me the moon",
        "find the moon", "locate the moon", "head to the moon",
        "go to luna", "take me to luna", "visit luna",
        "go to earth's moon", "take me to earth's satellite",
        "moon please", "luna please", "the moon now",
        "fly me to the moon", "take us to the moon"
    ],
    
    # JUPITER - Gas Giant
    "jupiter": [
        "go to jupiter", "take me to jupiter", "navigate to jupiter",
        "travel to jupiter", "fly to jupiter", "visit jupiter",
        "show me jupiter", "find jupiter", "locate jupiter",
        "go to the gas giant", "take me to the biggest planet",
        "navigate to the largest planet", "visit the giant planet",
        "jupiter please", "big jupiter", "huge jupiter",
        "go to jove", "take me to jove"  # Classical name
    ],
    
    # SATURN - Ringed Planet
    "saturn": [
        "go to saturn", "take me to saturn", "navigate to saturn",
        "travel to saturn", "fly to saturn", "visit saturn",
        "show me saturn", "find saturn", "locate saturn",
        "go to the ringed planet", "take me to the planet with rings",
        "navigate to the ring planet", "visit saturn's rings",
        "saturn please", "ringed saturn", "beautiful saturn"
    ],
    
    # SUN - Our Star
    "sun": [
        "go to the sun", "take me to the sun", "navigate to the sun",
        "travel to the sun", "fly to the sun", "visit the sun",
        "show me the sun", "find the sun", "locate the sun",
        "go to our star", "take me to our star", "navigate to sol",
        "go to sol", "take me to sol", "visit sol",  # Scientific name
        "sun please", "our sun", "the bright sun",
        "go to the center", "take me to the solar center"
    ],
    
    # VENUS - Morning/Evening Star
    "venus": [
        "go to venus", "take me to venus", "navigate to venus",
        "travel to venus", "fly to venus", "visit venus",
        "show me venus", "find venus", "locate venus",
        "go to the morning star", "take me to the evening star",
        "navigate to the bright planet", "visit the hottest planet",
        "venus please", "bright venus", "beautiful venus"
    ],
    
    # MERCURY - Innermost Planet
    "mercury": [
        "go to mercury", "take me to mercury", "navigate to mercury",
        "travel to mercury", "fly to mercury", "visit mercury",
        "show me mercury", "find mercury", "locate mercury",
        "go to the innermost planet", "take me to the closest planet to sun",
        "navigate to the fastest planet", "mercury please", "swift mercury"
    ],
    
    # NEPTUNE - Ice Giant
    "neptune": [
        "go to neptune", "take me to neptune", "navigate to neptune",
        "travel to neptune", "fly to neptune", "visit neptune",
        "show me neptune", "find neptune", "locate neptune",
        "go to the blue planet", "take me to the ice giant",
        "navigate to the windy planet", "neptune please", "distant neptune"
    ],
    
    # URANUS - Tilted Planet
    "uranus": [
        "go to uranus", "take me to uranus", "navigate to uranus",
        "travel to uranus", "fly to uranus", "visit uranus",
        "show me uranus", "find uranus", "locate uranus",
        "go to the tilted planet", "take me to the sideways planet",
        "navigate to the ice giant", "uranus please"
    ],
    
    # PLUTO - Dwarf Planet
    "pluto": [
        "go to pluto", "take me to pluto", "navigate to pluto",
        "travel to pluto", "fly to pluto", "visit pluto",
        "show me pluto", "find pluto", "locate pluto",
        "go to the dwarf planet", "take me to the distant world",
        "navigate to the edge", "pluto please", "far pluto"
    ],
    
    # STARS
    "alpha centauri": [
        "go to alpha centauri", "take me to alpha centauri",
        "navigate to alpha centauri", "visit alpha centauri",
        "go to the nearest star", "take me to the closest star",
        "alpha centauri please", "proxima centauri"
    ],
    
    "sirius": [
        "go to sirius", "take me to sirius", "navigate to sirius",
        "visit sirius", "show me sirius", "find sirius",
        "go to the brightest star", "take me to the dog star",
        "sirius please", "bright sirius"
    ],
    
    "betelgeuse": [
        "go to betelgeuse", "take me to betelgeuse", "navigate to betelgeuse",
        "visit betelgeuse", "show me betelgeuse", "find betelgeuse",
        "go to the red giant", "take me to the shoulder of orion",
        "betelgeuse please", "red betelgeuse"
    ],
    
    "vega": [
        "go to vega", "take me to vega", "navigate to vega",
        "visit vega", "show me vega", "find vega",
        "vega please", "bright vega"
    ],
    
    # SPACECRAFT
    "iss": [
        "go to the iss", "take me to the iss", "navigate to the iss",
        "visit the iss", "find the iss", "locate the iss",
        "go to the international space station", 
        "take me to the international space station",
        "navigate to the space station", "visit the space station",
        "iss please", "space station please"
    ],
    
    "hubble": [
        "go to hubble", "take me to hubble", "navigate to hubble",
        "visit hubble", "find hubble", "locate hubble",
        "go to the hubble telescope", "take me to the hubble telescope",
        "navigate to hubble space telescope", "hubble please"
    ]
}

# ==================== LANDING COMMANDS ====================

LANDING_TEST_CASES = {
    "moon": [
        "land on the moon", "land on moon", "touch down on the moon",
        "set down on the moon", "descend to the moon", "land at the moon",
        "put me down on the moon", "take me down to the moon",
        "moon landing", "land luna", "touchdown moon",
        "descend to luna", "set down on luna"
    ],
    
    "mars": [
        "land on mars", "land on the mars", "touch down on mars",
        "set down on mars", "descend to mars", "land at mars",
        "put me down on mars", "take me down to mars",
        "mars landing", "touchdown mars", "descend to the red planet",
        "land on the red planet", "set down on the red planet"
    ],
    
    "earth": [
        "land on earth", "land on the earth", "touch down on earth",
        "return to earth surface", "descend to earth", "land home",
        "touch down home", "return to ground", "land back on earth"
    ],
    
    "europa": [
        "land on europa", "touch down on europa", "descend to europa",
        "land on jupiter's moon", "set down on europa"
    ],
    
    "titan": [
        "land on titan", "touch down on titan", "descend to titan",
        "land on saturn's moon", "set down on titan"
    ]
}

# ==================== TRACKING COMMANDS ====================

TRACKING_TEST_CASES = {
    "jupiter": [
        "track jupiter", "follow jupiter", "keep an eye on jupiter",
        "watch jupiter", "focus on jupiter", "monitor jupiter",
        "stay with jupiter", "lock onto jupiter", "jupiter tracking"
    ],
    
    "saturn": [
        "track saturn", "follow saturn", "keep an eye on saturn",
        "watch saturn", "focus on saturn", "monitor saturn",
        "track the rings", "follow the ringed planet"
    ],
    
    "moon": [
        "track the moon", "follow the moon", "keep an eye on the moon",
        "watch the moon", "focus on the moon", "monitor the moon",
        "track luna", "follow luna"
    ],
    
    "mars": [
        "track mars", "follow mars", "keep an eye on mars",
        "watch mars", "focus on mars", "monitor mars",
        "track the red planet", "follow the red planet"
    ],
    
    "iss": [
        "track the iss", "follow the iss", "keep an eye on the iss",
        "watch the space station", "follow the space station",
        "track the international space station"
    ]
}

# ==================== EXPLORATION COMMANDS ====================

EXPLORATION_TEST_CASES = {
    "venus": [
        "explore venus", "investigate venus", "examine venus",
        "study venus", "discover venus", "check out venus",
        "explore the morning star", "investigate the hottest planet"
    ],
    
    "mars": [
        "explore mars", "investigate mars", "examine mars",
        "study mars", "discover mars", "check out mars",
        "explore the red planet", "investigate the red planet"
    ],
    
    "jupiter": [
        "explore jupiter", "investigate jupiter", "examine jupiter",
        "study jupiter", "discover jupiter", "check out jupiter",
        "explore the gas giant", "investigate the largest planet"
    ],
    
    "saturn": [
        "explore saturn", "investigate saturn", "examine saturn",
        "study saturn", "discover saturn", "check out saturn",
        "explore the rings", "investigate the ringed planet"
    ]
}

# ==================== PHOTOGRAPHY COMMANDS ====================

PHOTOGRAPHY_TEST_CASES = [
    # Direct screenshot commands
    "take a screenshot", "take screenshot", "screenshot",
    "capture image", "capture screen", "save image",
    "take a photo", "take photo", "photo",
    "take a picture", "take picture", "picture",
    "snap a picture", "snap picture", "snap photo",
    "save this view", "capture this view", "record this view",
    
    # Casual variations
    "screenshot please", "photo please", "picture please",
    "take a pic", "snap it", "capture it", "save it",
    "get a shot", "grab a screenshot", "make a picture",
    
    # With context
    "take a screenshot of this", "capture what we're seeing",
    "save what we're looking at", "photograph this view",
    "document this", "record this scene"
]

# ==================== RECOVERY COMMANDS ====================

RECOVERY_TEST_CASES = {
    "free_camera": [
        "free camera", "free the camera", "unlock camera",
        "unlock the camera", "release camera", "release the camera",
        "get unstuck", "unstuck camera", "camera unstuck",
        "liberate camera", "unfreeze camera", "camera free",
        "make camera free", "set camera free"
    ],
    
    "stop_camera": [
        "stop camera", "stop the camera", "halt camera",
        "halt the camera", "camera stop", "pause camera",
        "freeze camera", "hold camera", "camera halt"
    ],
    
    "back_to_space": [
        "back to space", "return to space", "get back to space",
        "go back to space", "return to the void", "back to the stars",
        "return to deep space", "get me out of here", "escape to space",
        "back to the cosmos", "return to the universe"
    ]
}

# ==================== MULTI-TOOL COMMANDS ====================

TOUR_TEST_CASES = {
    "solar_system": [
        "tour the solar system", "tour solar system", "grand tour",
        "solar system tour", "tour our solar system",
        "grand tour of the solar system", "complete solar system tour",
        "show me the solar system", "explore the solar system"
    ],
    
    "planets": [
        "tour the planets", "tour planets", "planet tour",
        "grand tour of planets", "tour all planets",
        "show me all planets", "visit all planets"
    ],
    
    "inner_planets": [
        "tour inner planets", "tour the inner planets",
        "inner planet tour", "rocky planet tour",
        "terrestrial planet tour"
    ],
    
    "outer_planets": [
        "tour outer planets", "tour the outer planets",
        "outer planet tour", "gas giant tour"
    ],
    
    "gas_giants": [
        "tour gas giants", "tour the gas giants",
        "gas giant tour", "giant planet tour"
    ]
}

CINEMATIC_TEST_CASES = {
    "mars": [
        "cinematic journey to mars", "movie journey to mars",
        "cinematic trip to mars", "dramatic journey to mars",
        "cinematic flight to mars", "movie-style trip to mars"
    ],
    
    "jupiter": [
        "cinematic journey to jupiter", "movie journey to jupiter",
        "cinematic approach to jupiter", "dramatic flight to jupiter"
    ]
}

STREAM_TOUR_TEST_CASES = {
    "jupiter": [
        "stream tour of jupiter", "streaming tour of jupiter",
        "live tour of jupiter", "jupiter stream tour",
        "stream tour of jupiter moons", "live jupiter exploration"
    ],
    
    "saturn": [
        "stream tour of saturn", "streaming tour of saturn",
        "live tour of saturn", "saturn stream tour",
        "stream tour of saturn rings", "live saturn exploration"
    ]
}

MULTI_STEP_TEST_CASES = [
    # Sequential commands
    "visit mars then land on it", "go to mars then land on it",
    "travel to mars and land on it", "fly to mars and touch down",
    "go to jupiter then track it", "visit jupiter and follow it",
    "navigate to saturn then explore it", "go to the moon and land on it",
    
    # Complex sequences
    "go to mars then take a screenshot", "visit jupiter then capture image",
    "travel to saturn then free camera", "explore venus then return to earth"
]

# ==================== PRONUNCIATION & SPEECH VARIATIONS ====================

SPEECH_VARIATIONS = {
    # Common speech-to-text errors
    "mars": ["mars", "mass", "marrs", "marz"],
    "venus": ["venus", "veenus", "venous"],
    "uranus": ["uranus", "your anus", "urine us"],  # Common mispronunciations
    "pluto": ["pluto", "pluton", "pludo"],
    "jupiter": ["jupiter", "jupitor", "jupe iter"],
    "saturn": ["saturn", "saternn", "sat urn"],
    "neptune": ["neptune", "nep tune", "neptuen"],
    "mercury": ["mercury", "mercery", "merkury"],
    
    # Common command variations
    "screenshot": ["screenshot", "screen shot", "scren shot"],
    "navigate": ["navigate", "navi gate", "naviaget"],
    "cinematic": ["cinematic", "cinema tic", "sinematic"]
}

# ==================== CONVERSATIONAL PATTERNS ====================

CONVERSATIONAL_TEST_CASES = [
    # Polite requests
    "could you please take me to mars",
    "would you mind going to jupiter",
    "can we visit saturn please",
    "i'd like to go to venus if possible",
    
    # Casual requests
    "hey go to mars", "yo take me to jupiter",
    "alright let's go to saturn", "ok visit venus now",
    
    # Excited/urgent
    "quickly go to mars", "fast travel to jupiter",
    "immediately take me to saturn", "hurry to venus",
    
    # Hesitant/uncertain
    "um go to mars", "uh take me to jupiter maybe",
    "well let's try saturn", "i guess go to venus",
    
    # With filler words
    "so like go to mars", "you know take me to jupiter",
    "basically visit saturn", "actually go to venus"
]

# ==================== EDGE CASES & DIFFICULT PRONUNCIATIONS ====================

DIFFICULT_TEST_CASES = [
    # Mumbled or unclear
    "g'to mars", "takeme jupiter", "gotosaturn",
    "screenshoot", "photoo", "picturee",
    
    # With background noise patterns (as might be transcribed)
    "go to mars um", "take me to jupiter uh",
    "visit saturn yeah", "explore venus ok",
    
    # Very casual/slurred
    "lemme go to mars", "wanna visit jupiter",
    "gonna explore saturn", "gotta see venus",
    
    # Multiple entities (ambiguous)
    "go to mars or jupiter", "visit saturn and venus",
    "explore jupiter then mars", "navigate between earth and mars"
]

# ==================== TEST EXECUTION FRAMEWORK ====================

def run_test_suite():
    """
    Execute comprehensive test suite for natural language processing
    """
    all_test_cases = {}
    
    # Combine all test cases
    all_test_cases.update({f"nav_{k}": v for k, v in NAVIGATION_TEST_CASES.items()})
    all_test_cases.update({f"land_{k}": v for k, v in LANDING_TEST_CASES.items()})
    all_test_cases.update({f"track_{k}": v for k, v in TRACKING_TEST_CASES.items()})
    all_test_cases.update({f"explore_{k}": v for k, v in EXPLORATION_TEST_CASES.items()})
    all_test_cases["photography"] = PHOTOGRAPHY_TEST_CASES
    all_test_cases.update({f"recovery_{k}": v for k, v in RECOVERY_TEST_CASES.items()})
    all_test_cases.update({f"tour_{k}": v for k, v in TOUR_TEST_CASES.items()})
    all_test_cases.update({f"cinematic_{k}": v for k, v in CINEMATIC_TEST_CASES.items()})
    all_test_cases.update({f"stream_{k}": v for k, v in STREAM_TOUR_TEST_CASES.items()})
    all_test_cases["multi_step"] = MULTI_STEP_TEST_CASES
    all_test_cases["conversational"] = CONVERSATIONAL_TEST_CASES
    all_test_cases["difficult"] = DIFFICULT_TEST_CASES
    
    return all_test_cases

def get_total_test_count():
    """Get total number of test cases"""
    test_cases = run_test_suite()
    total = 0
    for category, tests in test_cases.items():
        if isinstance(tests, dict):
            total += sum(len(v) for v in tests.values())
        else:
            total += len(tests)
    return total

if __name__ == "__main__":
    print(f"🎤 Natural Language Test Suite")
    print(f"📊 Total test cases: {get_total_test_count()}")
    print(f"📝 Categories: {len(run_test_suite())}")
    
    # Sample some test cases
    test_cases = run_test_suite()
    print(f"\n🔍 Sample Mars navigation commands:")
    for cmd in NAVIGATION_TEST_CASES["mars"][:5]:
        print(f"  • '{cmd}'")