# Morse Code Learning Application

A Python-based interactive Morse Code learning tool with audio playback, customizable settings, and comprehensive security features.

## Features

- 🎵 **Audio Morse Code Generation** - Real-time tone generation with PyAudio
- 🎓 **Interactive Learning** - Practice with random sequences and get instant feedback
- ⚙️ **Configurable Settings** - Customize timing, audio, and game parameters via JSON
- 🔒 **Security Hardened** - Input validation, resource limits, and comprehensive error handling
- 🎛️ **Character Set Control** - Choose from letters, numbers, and punctuation
- 🧵 **Multi-threaded Audio** - Non-blocking audio playback during interaction
- 📊 **Progress Tracking** - Score tracking with accuracy percentages

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

```bash
python morse.py
```

The application will start with default settings:
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
- **Configuration System**: JSON-based external settings
- **Security Layer**: Input validation and resource management
- **Audio Engine**: PyAudio integration with NumPy signal generation
- **Interactive System**: Multi-threaded user interaction

## File Structure

```
morse/
├── morse.py          # Main application
├── config.json       # Configuration settings
├── CONFIG.md         # Configuration documentation
├── CLAUDE.md         # Development documentation
└── README.md         # This file
```

## Dependencies

- **Python 3.6+**
- **PyAudio** - Audio playback and streaming
- **NumPy** - Signal generation and mathematical operations
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

### Input Problems
- Verify terminal supports raw input mode
- Check timeout settings in configuration
- Ensure proper terminal encoding

### Configuration Errors
- Validate JSON syntax
- Check parameter ranges in CONFIG.md
- Review security logs for validation errors

## Development

For development setup and architectural details, see `CLAUDE.md`.

For detailed configuration options, see `CONFIG.md`.

---

**Built with security in mind** 🔒 **Designed for learning** 📚 **Configurable by design** ⚙️