# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Morse Code learning application built in Python. The codebase consists of a single main file containing a MorseCode class that provides encoding, decoding, audio playback, and interactive learning features.

## Architecture

The application is structured around the `MorseCode` class in `morse.py` which handles:

- **Morse Code Dictionaries**: Separate dictionaries for letters, numbers, and punctuation that can be selectively enabled
- **Audio Engine**: Uses PyAudio and NumPy to generate and play Morse code tones with configurable timing
- **Interactive Learning**: Multi-threaded system that plays random Morse sequences and captures user input for verification
- **Configurable Character Sets**: Constructor allows enabling/disabling letters, numbers, and punctuation

Key components:
- `morse_dict_*`: Character-to-Morse mappings for different character types
- `inverse_morse_dict`: Morse-to-character mapping for decoding
- Audio streaming via PyAudio with real-time tone generation
- Threading for non-blocking audio playback during user interaction

## Running the Application

```bash
# Run the main application (currently configured for 20 rounds of 2-character sequences)
python morse.py
```

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

- `string_to_morse()`: Converts text to Morse code with '#' as character separator
- `play_string()`: Plays text as Morse audio
- `play_random_and_verify()`: Interactive learning method that plays random sequences
- `play_times()`: Runs multiple learning rounds with scoring

## Current Configuration

The main execution at the bottom runs:
- Letters only (no numbers or punctuation)
- 20 learning rounds
- 2-character sequences per round