# Morse Code Learning Application

A Python-based interactive Morse Code learning tool with audio playback, customizable settings, and comprehensive security features. Available in both command-line and graphical user interface (GUI) versions.

## Features

- 🎵 **Audio Morse Code Generation** - Real-time tone generation with PyAudio
- 🖥️ **Dual Interface** - Command-line and modern GUI versions available
- 🎓 **Interactive Learning** - Practice with random sequences and get instant feedback
- 📻 **QSO Practice** - Realistic amateur radio contact simulation with intelligent scoring
- ⚙️ **Configurable Settings** - Customize timing, audio, and game parameters via JSON
- 🔒 **Security Hardened** - Input validation, resource limits, and comprehensive error handling
- 🎛️ **Character Set Control** - Choose from letters, numbers, and punctuation
- 🧵 **Multi-threaded Audio** - Non-blocking audio playback during interaction
- 📊 **Progress Tracking** - Score tracking with accuracy percentages
- 🔄 **Text Converter** - Built-in text-to-Morse and Morse-to-text conversion
- 📖 **Abbreviation Glossary** - Searchable reference for 62 amateur radio abbreviations

## Quick Start

### Prerequisites

```bash
pip install pyaudio numpy
```

### Installation

```bash
git clone https://github.com/ettoreferranti/morse.git
cd morse
```

### Run the Application

#### GUI Version (Recommended)
```bash
python morse_gui.py
# or
python run_morse_gui.py
```

#### Command-Line Version
```bash
python morse.py
```

Both versions start with default settings:
- 20 practice rounds
- 2-character sequences
- Letters only (A-Z)
- 600 Hz audio tone

## Configuration

The application uses `config.json` for all settings. You can customize:

### Audio Settings
- **Frequency**: Tone frequency in Hz (default: 600)
- **Volume**: Audio volume level (0.0-1.0)
- **Sample Rate**: Audio sample rate (default: 44100)

### Timing Parameters
- **Speed**: Overall timing multiplier (default: 0.06)
- **Dit/Dah Ratios**: Relative durations for dots and dashes
- **Spacing**: Word and character spacing ratios

### Game Settings
- **Rounds**: Number of practice rounds (default: 20)
- **Sequence Length**: Characters per sequence (default: 2)
- **Character Sets**: Enable letters, numbers, punctuation

### QSO Practice Settings
- **QSO Count**: Number of QSOs per session (default: 5)
- **Verbosity**: QSO template verbosity - minimal/medium/chatty (default: medium)
- **Call Regions**: Optional filters for call sign regions (default: any)
- **Fuzzy Threshold**: Similarity threshold for partial credit (default: 0.8)
- **Partial Credit**: Enable partial credit scoring (default: true)
- **Case Sensitive**: Case-sensitive answer matching (default: false)

### Security Limits
- **Input Validation**: Maximum input lengths and timeouts
- **Resource Limits**: Thread limits and audio parameter bounds

## Example Configurations

### Beginner Setup (Slower Speed)
```json
{
  "timing": {
    "multiplier": 0.12
  },
  "game": {
    "default_rounds": 10,
    "default_sequence_length": 1
  }
}
```

### Advanced Practice (All Characters)
```json
{
  "character_sets": {
    "use_letters": true,
    "use_numbers": true,
    "use_punctuation": true
  },
  "game": {
    "default_rounds": 50,
    "default_sequence_length": 5
  }
}
```

### Custom Audio Settings
```json
{
  "audio": {
    "frequency": 800,
    "volume": 0.8
  },
  "timing": {
    "multiplier": 0.04
  }
}
```

## GUI Features

The graphical user interface provides an intuitive way to use all application features:

### Practice Tab
- **Interactive Practice Area** - Visual feedback and real-time scoring
- **Configurable Sessions** - Set rounds, sequence length, and character sets
- **Progress Tracking** - Live progress bar and detailed results history
- **Audio Controls** - Play, replay, and stop functionality
- **Auto-submission** - Automatically advances when sequence is complete

### Configuration Tab
- **Real-time Settings** - Adjust audio frequency, volume, and timing speed
- **Visual Sliders** - Easy-to-use controls for all parameters
- **Configuration Management** - Load, save, and reset configuration files
- **Live Preview** - See configuration changes in real-time

### Text Converter Tab
- **Bidirectional Conversion** - Text-to-Morse and Morse-to-text
- **Audio Playback** - Play any converted Morse code
- **Large Text Support** - Handle long messages with scrollable text areas

### GUI Benefits
- **User-Friendly** - No command-line experience required
- **Visual Feedback** - Clear progress indicators and status messages
- **Error Handling** - Friendly error messages with helpful suggestions
- **Multi-tasking** - Non-blocking audio allows continued interaction

### QSO Practice Tab
- **Realistic Amateur Radio Contacts** - Practice copying authentic QSO conversations
- **Session Configuration** - Customize QSO count, verbosity, and call sign regions
- **Interactive Transcription** - Fill in callsigns, names, QTHs, RST reports, and equipment details
- **Intelligent Scoring** - Fuzzy matching with partial credit for close answers
- **Abbreviation Glossary** - Searchable reference for 62 amateur radio abbreviations
- **Progress Tracking** - Real-time session progress and cumulative scoring
- **Audio Controls** - Play, replay, skip, and stop functionality
- **Multi-Level Practice** - Choose from minimal, medium, or chatty QSO templates

#### QSO Feature Highlights
- **9 Call Sign Regions** - US, UK, DE, FR, VK, JA, ON, PA, I with realistic formats
- **62 Abbreviations** - Common amateur radio abbreviations categorized by type
- **Fuzzy Matching** - Configurable similarity threshold (0.5-1.0) for forgiving scoring
- **Partial Credit** - Award points for close answers, not just exact matches
- **Element Tracking** - Track accuracy per element type (callsign, name, QTH, RST, etc.)
- **Session Statistics** - View overall accuracy and detailed element-by-element performance

## Usage Examples

### Basic Usage
```python
from morse import MorseCode

# Use default configuration
morse = MorseCode()
morse.play_times(20, 2)  # 20 rounds, 2 characters each
```

### Custom Configuration
```python
# Use specific config file
morse = MorseCode(config_file='my_settings.json')

# Override character sets
morse = MorseCode(use_letters=True, use_numbers=True)

# Practice with custom parameters
morse.play_times(rounds=50, length=3)
```

### Convert and Play Text
```python
morse = MorseCode()

# Convert text to Morse code
morse_code = morse.string_to_morse("HELLO WORLD")
print(morse_code)  # Output: ....#.#.-..#.-..#---# .--#---#.-.#.-..#-#

# Play text as audio
morse.play_string("SOS")
```

## Security Features

The application includes comprehensive security measures:

- **Input Validation**: Length limits and type checking
- **Resource Protection**: Thread limits and audio parameter bounds
- **Timeout Handling**: Prevents indefinite blocking
- **Error Recovery**: Graceful handling of invalid inputs
- **Audit Logging**: Security events logged with timestamps

## Architecture

- **MorseCode Class**: Core functionality with audio generation
- **GUI Interface**: Modern tkinter-based graphical user interface
- **Configuration System**: JSON-based external settings
- **Security Layer**: Input validation and resource management
- **Audio Engine**: PyAudio integration with NumPy signal generation
- **Interactive System**: Multi-threaded user interaction

## File Structure

```
morse/
├── morse.py          # Command-line application
├── morse_gui.py      # GUI application  
├── run_morse_gui.py  # GUI launcher script
├── config.json       # Configuration settings
├── CONFIG.md         # Configuration documentation
├── CLAUDE.md         # Development documentation
└── README.md         # This file
```

## Dependencies

- **Python 3.6+**
- **PyAudio** - Audio playback and streaming
- **NumPy** - Signal generation and mathematical operations
- **tkinter** - GUI interface (included with most Python installations)
- **Built-in modules**: `json`, `threading`, `termios`, `logging`

## Platform Support

- **macOS**: Full support with terminal audio
- **Linux**: Full support with ALSA/PulseAudio
- **Windows**: Requires PyAudio Windows installation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with security considerations
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## License

This project is open source. See the repository for license details.

## Troubleshooting

### Audio Issues
- Ensure PyAudio is properly installed
- Check system audio permissions
- Try different audio frequencies in config

### GUI Issues
- Ensure tkinter is installed (usually comes with Python)
- Check system display settings and permissions
- Try running `python run_morse_gui.py` for better error reporting

### Input Problems (Command-line)
- Verify terminal supports raw input mode
- Check timeout settings in configuration
- Ensure proper terminal encoding

### Configuration Errors
- Validate JSON syntax
- Check parameter ranges in CONFIG.md
- Review security logs for validation errors
- Use GUI Configuration tab for easier setup

## Development

For development setup and architectural details, see `CLAUDE.md`.

For detailed configuration options, see `CONFIG.md`.

---

**Built with security in mind** 🔒 **Designed for learning** 📚 **Configurable by design** ⚙️