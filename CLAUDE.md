# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Morse Code learning application built in Python. The codebase consists of a single main file containing a MorseCode class that provides encoding, decoding, audio playback, and interactive learning features.

## Architecture

The application is structured around the `MorseCode` class in `morse.py` which handles:

- **Morse Code Dictionaries**: Separate dictionaries for letters, numbers, and punctuation that can be selectively enabled
- **Audio Engine**: Uses PyAudio and NumPy to generate and play Morse code tones with configurable timing
- **Interactive Learning**: Multi-threaded system that plays random Morse sequences and captures user input for verification
- **External Configuration**: JSON-based configuration system for timing, audio, and security settings
- **Security Features**: Input validation, resource limits, and comprehensive error handling

Key components:
- `morse_dict_*`: Character-to-Morse mappings for different character types
- `inverse_morse_dict`: Morse-to-character mapping for decoding
- Audio streaming via PyAudio with real-time tone generation
- Threading for non-blocking audio playback during user interaction

## Running the Application

```bash
# Run with default configuration (loaded from config.json)
python morse.py
```

## Configuration

The application uses a `config.json` file for all settings:
- Timing parameters (dit/dah durations, spacing)
- Audio settings (frequency, volume, sample rate)  
- Security limits (input validation, thread limits)
- Game parameters (rounds, sequence length)
- Character sets (letters, numbers, punctuation)

See `CONFIG.md` for detailed configuration options.

## Dependencies

Required Python packages:
- `pyaudio` - Audio playback
- `numpy` - Signal generation
- `termios`, `tty` - Terminal input handling (Unix/Linux/macOS)

Install dependencies:
```bash
pip install pyaudio numpy
```

## Key Methods

- `string_to_morse()`: Converts text to Morse code with input validation and length limits
- `play_string()`: Plays text as Morse audio using configured timing
- `play_random_and_verify()`: Interactive learning method with timeout handling
- `play_times()`: Runs multiple learning rounds with comprehensive error handling
- `reload_config()`: Dynamically reload configuration without restarting

## Default Configuration

The application starts with these defaults (from `config.json`):
- Letters only (no numbers or punctuation)
- 20 learning rounds
- 2-character sequences per round
- 600 Hz audio frequency
- Comprehensive security limits enabled