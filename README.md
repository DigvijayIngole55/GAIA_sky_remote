# 🚀 Standalone Gaia Sky Remote Controller

A completely independent, LLM-powered natural language remote controller for Gaia Sky with advanced multi-tool capabilities and **direct voice control**!

> **📚 For detailed documentation, see [docs/README.md](docs/README.md)**

## ✨ Features

### 🎤 **Direct Voice Control - No Wake Word!**
- **Natural speech**: Just say `"Take me to Mars"`
- **Hands-free**: Pure voice mode available
- **High accuracy**: Whisper Base model
- **Direct commands**: No wake words needed

### 🎯 **Single Tool Commands**
- **Navigation**: `go to mars`, `fly to jupiter`, `visit saturn`
- **Landing**: `land on the moon`, `touch down on europa`
- **Tracking**: `track saturn`, `follow jupiter`, `watch the moon`
- **Exploration**: `explore venus`, `investigate mars` (cinematic mode)
- **Photos**: `take screenshot`, `capture image`, `save this view`

### 🎬 **Multi-Tool Sequences** (NEW!)
- **🗺️ Grand Tours**: `tour the solar system`, `grand tour of planets`
- **📺 Stream Tours**: `stream tour of jupiter moons` (live commentary)
- **🎬 Cinematic**: `cinematic journey to mars` (5-step movie sequence)
- **🔄 Multi-Step**: `visit mars then land on it` (parsed chains)

### 🆘 **Recovery Commands**
- **Get Unstuck**: `free camera`, `unlock camera`, `get unstuck`
- **Stop Motion**: `stop camera`, `back to space`

## 🛠️ Setup

### Prerequisites
1. **Gaia Sky** - Running with Python bridge enabled
2. **LM Studio** - With `google/gemma-3-4b-it` model loaded on port 1234
3. **Python 3.8+**
4. **Microphone** - For voice control (optional)

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the controller
python remote_controller.py
```

## 🎮 Usage

### Quick Start Options

#### 1. **Main Controller** (Recommended)
```bash
python scripts/remote_controller.py
# Choose from 3 control modes
```

#### 2. **Pure Voice Control** 🎤
```bash
python scripts/voice_controller.py
# Hands-free space exploration
```

#### 3. **Test Setup**
```bash
python tests/test_speech_setup.py
# Verify speech recognition works
```

### Example Commands

#### Text Commands
```
🌌 Command: go to mars
⚡ Processing: go to mars
🎯 ✈️ Traveling to Mars... Enjoy the journey through space!

🌌 Command: tour the solar system
⚡ Processing: tour the solar system
🎯 🎬 Starting solar system tour with 9 stops...
    📍 Route: Sun → Mercury → Venus → Earth → Mars → Jupiter → Saturn → Uranus → Neptune
```

#### Voice Commands 🎤 **NEW: No Wake Word!**
```
🎤 Say: "Take me to Mars"
🚀 Voice Result: ✈️ Traveling to Mars... Enjoy the journey through space!

🎤 Say: "Tour the solar system"  
🚀 Voice Result: 🎬 Starting solar system tour with 9 stops...

🎤 Say: "Land on the Moon"
🚀 Voice Result: 🛬 Landing on Moon... Touchdown successful!
```

### Advanced Multi-Tool Examples
```
# Epic space tours
tour the solar system
grand tour of planets
tour inner planets
tour gas giants

# Cinematic experiences  
cinematic journey to mars
stream tour of jupiter moons
stream tour of saturn rings

# Multi-step commands
visit mars then land on it
go to jupiter and track it

# Recovery (when stuck)
free camera
get unstuck
back to space
```

## 🧠 How It Works

### Dual Parsing System
1. **LLM Parsing** - Uses LM Studio with Gemma 3:4B for intelligent command understanding
2. **Regex Fallback** - Extensive pattern matching for reliability

### Natural Language Understanding
- **Celestial Aliases**: `red planet` → Mars, `gas giant` → Jupiter
- **Action Variations**: `go to`, `take me to`, `fly to`, `travel to`
- **Complex Commands**: `visit mars then land on it` automatically parsed

### Connection Management
- **Persistent Connection** - Single connection throughout session
- **Auto-Reconnect** - Handles connection issues gracefully
- **Thread-Safe** - Safe for concurrent operations

## 📂 Files

```
standalone_remote_control/
├── remote_controller.py      # Main controller (complete!)
├── gaia_sky_connection.py    # Minimal connection manager
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🎯 What Makes This Special

### 🔥 **Complete Independence**
- **No parent dependencies** - Runs completely standalone
- **Minimal footprint** - Only essential components extracted
- **Self-contained** - Everything needed in one folder

### ⚡ **Performance Optimized**
- **Persistent connections** - No reconnection overhead
- **Direct API calls** - Minimal latency
- **Streaming execution** - Real-time feedback

### 🎬 **Advanced Capabilities**
- **Multi-tool sequences** - Complex coordinated actions
- **Iterative streaming** - Live updates during execution
- **Natural language** - Understands 100+ command variations

## 🚀 Commands Reference

### Navigation
```
go to mars                    # Basic navigation
take me to jupiter           # Natural variation
fly to saturn               # Action synonym
travel to the sun           # Alternative phrasing
navigate to venus           # Formal style
visit earth                 # Casual style
show me pluto              # Discovery style
```

### Multi-Tool Tours
```
tour the solar system       # 9-stop grand tour
tour inner planets          # Mercury → Venus → Earth → Mars  
tour gas giants             # Jupiter → Saturn → Uranus → Neptune
stream tour of jupiter moons # Io → Europa → Ganymede → Callisto
cinematic journey to mars   # 5-step movie sequence
```

### Recovery
```
free camera                 # Unlock stuck camera
get unstuck                # Alternative phrasing
back to space              # Return from surface
stop camera                # Halt all movement
```

## 💡 Tips

1. **If stuck after landing**: Use `free camera` or `back to space`
2. **For epic exploration**: Try `stream tour of jupiter moons`
3. **For help**: Type `help` anytime for full command list
4. **Multi-step commands**: Use `then` or `and` to chain actions

## 🎉 Ready to Explore!

This standalone controller gives you the full power of natural language space exploration with advanced multi-tool capabilities - all in one independent package!

**The universe awaits your commands!** 🌌