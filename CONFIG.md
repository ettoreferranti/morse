# Configuration Guide

The Morse Code application now supports external configuration through a `config.json` file. This allows you to customize timing, audio settings, security parameters, and game behavior without modifying the source code.

## Configuration File Location

The application looks for `config.json` in:
1. Current working directory (first priority)
2. Same directory as the script file (fallback)

If no config file is found, the application uses built-in defaults.

## Configuration Structure

### Audio Settings
```json
"audio": {
  "frequency": 600,      // Morse tone frequency in Hz (50-5000)
  "sample_rate": 44100,  // Audio sample rate in Hz (8000-96000)
  "volume": 1.0          // Audio volume (0.0-1.0)
}
```

### Timing Settings
```json
"timing": {
  "multiplier": 0.06,                    // Base timing multiplier
  "dit_duration_ratio": 1.2,            // Dit length relative to multiplier
  "dah_duration_ratio": 2.5,            // Dah length relative to multiplier  
  "space_between_words_ratio": 4.0,     // Word spacing relative to multiplier
  "space_between_characters_ratio": 3.0, // Character spacing relative to multiplier
  "space_between_dit_dah_ratio": 0.2,   // Dit/dah spacing relative to multiplier
  "round_delay": 0.5                     // Delay between game rounds in seconds
}
```

**Timing Calculation**: 
- Dit duration = `multiplier * dit_duration_ratio`
- Dah duration = `multiplier * dah_duration_ratio`
- etc.

### Security Settings
```json
"security": {
  "max_input_length": 1000,        // Maximum characters in input strings
  "max_threads": 5,                // Maximum concurrent audio threads
  "input_timeout": 30,             // General input timeout in seconds
  "character_input_timeout": 60,   // Per-character input timeout in seconds
  "min_frequency": 50,             // Minimum allowed audio frequency
  "max_frequency": 5000,           // Maximum allowed audio frequency
  "min_duration": 0.001,           // Minimum tone duration in seconds
  "max_duration": 10.0,            // Maximum tone duration in seconds
  "max_rounds": 100,               // Maximum game rounds allowed
  "max_sequence_length": 10        // Maximum sequence length per round
}
```

### Game Settings
```json
"game": {
  "default_rounds": 20,           // Default number of practice rounds
  "default_sequence_length": 2    // Default character sequence length
}
```

### Character Sets
```json
"character_sets": {
  "use_letters": true,      // Include A-Z in practice
  "use_numbers": false,     // Include 0-9 in practice
  "use_punctuation": false, // Include punctuation marks
  "custom_characters": []   // Optional: specify exact characters to use
}
```

### QSO Practice Settings
```json
"qso": {
  "default_qso_count": 5,       // Default number of QSOs per session (1-20)
  "default_verbosity": "medium", // QSO template verbosity: minimal, medium, or chatty
  "default_call_region1": null,  // Optional call sign region filter (US, UK, DE, FR, VK, JA, ON, PA, I)
  "default_call_region2": null,  // Optional second call sign region filter
  "fuzzy_threshold": 0.8,        // Similarity threshold for partial credit (0.5-1.0)
  "partial_credit": true,        // Award partial credit for close answers
  "case_sensitive": false        // Case-sensitive answer matching
}
```

**QSO Verbosity Levels**:
- `minimal`: Short QSOs with required elements only (callsigns, names, QTHs, RSTs)
- `medium`: Standard QSOs including some equipment details
- `chatty`: Detailed QSOs with full equipment specs and additional exchanges

**Fuzzy Matching**:
- `1.0`: Exact match required (no tolerance)
- `0.9`: Very strict (callsign default - allows minor typos)
- `0.8`: Standard (general default - forgiving for common mistakes)
- `0.5`: Very lenient (accepts significantly different answers)

## Usage Examples

### Basic Usage
```python
# Uses config.json with all defaults
morse = MorseCode()
morse.play_times(20, 2)
```

### Custom Configuration
```python
# Use specific config file
morse = MorseCode(config_file='my_config.json')

# Override character sets
morse = MorseCode(use_letters=True, use_numbers=True)
```

### Runtime Configuration Changes
```python
morse = MorseCode()

# Modify settings and reload
morse.reload_config('new_config.json')
```

## Common Customizations

### Slower Practice Speed
```json
"timing": {
  "multiplier": 0.12,  // Double the timing for slower practice
  "dit_duration_ratio": 1.2,
  "dah_duration_ratio": 2.5,
  // ... other ratios unchanged
}
```

### Higher Frequency Tone
```json
"audio": {
  "frequency": 800,  // Higher pitch tone
  "sample_rate": 44100,
  "volume": 1.0
}
```

### Advanced Practice Settings
```json
"game": {
  "default_rounds": 50,
  "default_sequence_length": 5
},
"character_sets": {
  "use_letters": true,
  "use_numbers": true,
  "use_punctuation": true
}
```

## Error Handling

- **Invalid JSON**: Falls back to default configuration
- **Missing sections**: Uses defaults for missing parts
- **Invalid values**: Validates ranges and falls back to defaults
- **Missing file**: Creates default configuration automatically

## Configuration Validation

The application validates:
- Audio frequency (50-5000 Hz)
- Sample rate (8000-96000 Hz)  
- Positive timing multiplier
- All required configuration sections

Invalid configurations are logged and replaced with safe defaults.

## Security Features

Configuration-based security limits prevent:
- Resource exhaustion attacks
- Audio system abuse
- Excessive input lengths  
- Thread proliferation
- Denial of service attempts

All security parameters can be adjusted in the config file while maintaining protection.