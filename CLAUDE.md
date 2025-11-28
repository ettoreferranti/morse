# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Morse Code learning application built in Python. The project provides both command-line and GUI interfaces for learning Morse code through interactive audio-based practice sessions. The application features comprehensive security, configurable settings, and a robust audio engine.

## Project Structure

```
morse/
├── morse.py           # Core MorseCode class and CLI application (main logic)
├── morse_gui.py       # GUI application using tkinter
├── run_morse_gui.py   # GUI launcher script with error handling
├── config.json        # External configuration file
├── CONFIG.md          # Configuration documentation
├── CLAUDE.md          # This file (development guidance)
└── README.md          # User documentation
```

## Architecture

### Core Components

#### 1. MorseCode Class (`morse.py`)
The main class that handles all Morse code operations:

- **Morse Code Dictionaries**: Three separate dictionaries (`morse_dict_letters`, `morse_dict_numbers`, `morse_dict_punctuation`) that can be selectively enabled or combined
- **Custom Character Support**: Allows specifying a custom subset of characters to use
- **Audio Engine**: PyAudio-based real-time tone generation with NumPy for waveform synthesis
- **Interactive Learning System**: Multi-threaded audio playback with terminal input capture
- **External Configuration**: JSON-based settings loaded at initialization with runtime reloading
- **Security Layer**: Comprehensive input validation, resource limits, and error handling
- **Timeout Management**: Configurable timeouts for user input to prevent blocking

Key data structures:
- `morse_dict`: Combined dictionary of enabled character sets mapping characters → Morse patterns
- `inverse_morse_dict`: Reverse lookup mapping Morse patterns → characters
- `config`: Dictionary containing all settings loaded from JSON
- `active_threads`: List tracking audio playback threads for resource management

#### 2. GUI Application (`morse_gui.py`)
Tkinter-based graphical interface with three main tabs:

- **Practice Tab**: Interactive learning with visual feedback, progress tracking, and session configuration
- **Configuration Tab**: Real-time settings adjustment with sliders and save/load functionality
- **Text Converter Tab**: Bidirectional text/Morse conversion with audio playback

The GUI runs audio playback in separate threads to maintain UI responsiveness.

#### 3. Configuration System (`config.json`)
Hierarchical JSON configuration with six main sections:

1. **audio**: Frequency (Hz), sample rate, volume
2. **timing**: Speed multiplier and duration ratios for dits, dahs, and spacing
3. **security**: Input validation limits, timeouts, resource bounds
4. **game**: Default practice session parameters
5. **character_sets**: Boolean flags for letters/numbers/punctuation + custom characters array
6. All parameters have validated ranges and defaults

## Running the Application

### GUI Version (Recommended)
```bash
python morse_gui.py
# or
python run_morse_gui.py  # With additional error handling
```

### Command-Line Version
```bash
python morse.py
```

Both load settings from `config.json` automatically.

## Key Methods and Functions

### MorseCode Class Core Methods

**Initialization & Configuration:**
- `__init__(use_letters, use_numbers, use_punctuation, custom_characters, config_file)`: Initialize with optional overrides for config settings (morse.py:61)
- `_load_config(config_file)`: Load and validate JSON configuration (morse.py:140)
- `_sanitize_config_path(file_path)`: Security validation for config file paths (morse.py:179)
- `_validate_config(config)`: Validate configuration structure and ranges (morse.py:258)
- `reload_config(config_file)`: Hot-reload configuration without restarting (morse.py:488)

**Conversion Methods:**
- `to_morse(char)`: Convert single character to Morse pattern (morse.py:276)
- `from_morse(morse_code)`: Convert Morse pattern to character (morse.py:279)
- `string_to_morse(input_string, max_length)`: Convert string to Morse with validation (morse.py:326)
- `morse_to_string(morse_string)`: Convert Morse string back to text (morse.py:352)

**Audio Playback:**
- `play_tone(frequency, duration)`: Generate and play a single tone with validation (morse.py:282)
- `play_morse(message)`: Play Morse code string as audio tones (morse.py:313)
- `play_string(message)`: Convert text to Morse and play (morse.py:310)

**Interactive Learning:**
- `getch(timeout)`: Capture single character with timeout for Unix terminals (morse.py:379)
- `play_random_and_verify(length)`: Play random sequence and verify user input (morse.py:404)
- `play_times(times, length)`: Run multiple practice rounds with scoring (morse.py:452)

**Cleanup:**
- `__del__()`: Safe cleanup of audio streams and threads (morse.py:355)

### GUI Class Key Methods (morse_gui.py)

- `create_practice_tab()`: Build interactive practice interface with controls
- `create_config_tab()`: Build configuration editor with sliders
- `create_converter_tab()`: Build text/Morse converter interface
- `start_practice_session()`: Initialize and run practice rounds
- `submit_answer()`: Process user answer and update score
- `load_config_from_file()`: Load JSON config into GUI controls
- `save_config_to_file()`: Save current GUI settings to JSON
- `update_morse_instance()`: Recreate MorseCode instance with new settings

## Security Features

The application implements multiple security layers:

1. **Input Validation**: All user inputs validated for type, length, and content (morse.py:326-350)
2. **Path Sanitization**: Config file paths checked for traversal attacks (morse.py:179-216)
3. **Resource Limits**: Thread count limits, audio parameter bounds, timeout enforcement
4. **Parameter Validation**: Audio frequency (50-5000 Hz), duration (0.001-10s), sequence length (1-10), rounds (1-100)
5. **Error Handling**: Try-catch blocks with logging for all critical operations
6. **Timeout Protection**: Configurable timeouts prevent indefinite blocking on user input
7. **Audit Logging**: Security events logged with timestamps using Python logging module

## Configuration System

### Loading Priority
1. Constructor parameters (highest priority)
2. Specified config file (`config_file` parameter)
3. `config.json` in current directory
4. `config.json` in script directory
5. Hard-coded defaults (fallback)

### Configuration Sections

**Audio Settings** (config.json:2-6):
- `frequency`: Tone frequency in Hz (50-5000)
- `sample_rate`: Audio sample rate (8000-96000)
- `volume`: Output volume (0.0-1.0)

**Timing Settings** (config.json:7-15):
- `multiplier`: Overall speed factor (>0)
- `*_ratio` values: Relative durations for Morse timing

**Security Settings** (config.json:16-27):
- Input limits, timeouts, and resource bounds
- All enforced at runtime with logging

**Game Settings** (config.json:28-31):
- Default practice session parameters

**Character Sets** (config.json:32-37):
- Boolean flags to enable letter/number/punctuation sets
- `custom_characters` array for specific character subsets

## Dependencies

### Required Packages
- `pyaudio` - Audio I/O and streaming
- `numpy` - Waveform generation and signal processing
- `tkinter` - GUI framework (usually included with Python)

### Built-in Modules
- `json` - Configuration parsing
- `threading` - Non-blocking audio playback
- `termios`, `tty` - Raw terminal input (Unix/Linux/macOS only)
- `logging` - Security audit trail
- `time`, `random`, `sys`, `os`, `re`, `select` - Standard utilities

### Installation
```bash
pip install pyaudio numpy
```

## Default Configuration

Application defaults (from config.json):
- **Character Set**: Letters only (A-Z)
- **Practice**: 20 rounds of 2-character sequences
- **Audio**: 600 Hz at 44100 Hz sample rate, full volume
- **Speed**: 0.06 multiplier (moderate pace)
- **Security**: All limits enabled with conservative values

## Development Notes

### Code Style
- Single main class (`MorseCode`) with clear method responsibilities
- Extensive inline comments explaining security measures
- Comprehensive docstrings for public methods
- Configuration-driven design for flexibility

### Testing Considerations
- Test with different character set combinations
- Verify security limits prevent resource exhaustion
- Test config file validation and fallback behavior
- Verify audio playback across different platforms
- Test timeout handling and thread cleanup

### Platform Compatibility
- **macOS/Linux**: Full support with terminal input
- **Windows**: PyAudio requires specific installation; terminal input methods may need adaptation

### Future Enhancement Areas
- Windows-compatible input handling (replace termios/tty)
- Additional audio waveforms (square wave, etc.)
- Visual Morse code display option
- Progress tracking and statistics persistence
- Web-based interface option
- Additional language character sets (non-English)

## Common Development Tasks

### Adding New Character Sets
1. Create new dictionary (e.g., `morse_dict_special`) in `__init__` (morse.py:77-87)
2. Add boolean flag to config.json character_sets section
3. Update dictionary merge logic (morse.py:89-114)
4. Add GUI controls if updating GUI version

### Modifying Audio Generation
- Audio synthesis in `play_tone()` (morse.py:282-308)
- Uses NumPy sine wave generation
- PyAudio stream configured at initialization (morse.py:122-126)

### Adjusting Security Limits
- Modify ranges in `_validate_config()` (morse.py:258-274)
- Update corresponding checks in methods (e.g., `play_tone()`, `string_to_morse()`)
- Update `_get_default_config()` with new defaults (morse.py:218-256)

### Extending GUI
- Tab creation in `__init__` method (morse_gui.py:24+)
- Each tab has dedicated creation method
- Use threading for blocking operations to maintain UI responsiveness

## Important Implementation Details

1. **Thread Safety**: Audio playback runs in daemon threads; cleanup handled in `__del__`
2. **Timing Model**: All timing based on ratios multiplied by configurable base multiplier
3. **Morse Encoding**: Uses `#` for inter-character space, regular space for word separation
4. **Character Mapping**: All input converted to uppercase for dictionary lookup
5. **Config Reloading**: Can reload config at runtime without restarting application
6. **Custom Characters**: When set, override the boolean character set flags completely