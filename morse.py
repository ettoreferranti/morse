import time
import pyaudio
import numpy as np
import random
import sys
import termios
import tty
import threading
import select
import logging
import json
import os
import re

class MorseCode:
    """
    A class to represent Morse Code operations including encoding, decoding, and playing Morse code tones.

    Attributes
    ----------
    morse_dict : dict
        A dictionary mapping characters to their Morse code equivalents.
    inverse_morse_dict : dict
        A dictionary mapping Morse code to their character equivalents.
    p : pyaudio.PyAudio
        An instance of PyAudio for audio operations.
    stream : pyaudio.Stream
        An audio stream for playing tones.
    dit_duration : float
        Duration of a dit (short beep) in seconds.
    dah_duration : float
        Duration of a dah (long beep) in seconds.
    space_between_words : float
        Duration of space between words in seconds.
    space_between_characters : float
        Duration of space between characters in seconds.
    space_between_dit_dah : float
        Duration of space between dits and dahs in seconds.

    Methods
    -------
    to_morse(char):
        Converts a character to its Morse code equivalent.
    from_morse(morse_code):
        Converts a Morse code to its character equivalent.
    play_tone(frequency, duration):
        Plays a tone of a given frequency and duration.
    play_string(message):
        Converts a string message to Morse code and plays it.
    play_morse(message):
        Plays a Morse code message.
    string_to_morse(input_string):
        Converts a string to its Morse code equivalent.
    morse_to_string(morse_string):
        Converts a Morse code string to its character equivalent.
    __del__():
        Cleans up the audio stream and terminates the PyAudio instance.
    reload_config():
        Reloads configuration from the config file.
    """
    def __init__(self, use_letters=None, use_numbers=None, use_punctuation=None, custom_characters=None, config_file='config.json'):
        # Setup security logging
        logging.basicConfig(level=logging.WARNING, format='%(asctime)s - SECURITY - %(message)s')
        
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Override config with constructor parameters if provided
        if use_letters is not None:
            self.config['character_sets']['use_letters'] = use_letters
        if use_numbers is not None:
            self.config['character_sets']['use_numbers'] = use_numbers
        if use_punctuation is not None:
            self.config['character_sets']['use_punctuation'] = use_punctuation
        if custom_characters is not None:
            self.config['character_sets']['custom_characters'] = custom_characters
        self.morse_dict_letters = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..'}
        self.morse_dict_numbers = {
            '0': '-----', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.'}
        self.morse_dict_punctuation = {
            '.': '.-.-.-', ',': '--..--', '?': '..--..', '/': '-..-.'}

        # Select which dictionaries to include based on config
        custom_chars = self.config['character_sets'].get('custom_characters', [])
        
        if custom_chars:
            # Use custom character set - override other settings
            self.morse_dict = {}
            # Create combined dictionary of all possible characters
            all_chars = {}
            all_chars.update(self.morse_dict_letters)
            all_chars.update(self.morse_dict_numbers)
            all_chars.update(self.morse_dict_punctuation)
            
            # Add only the custom characters that exist in our dictionaries
            for char in custom_chars:
                char_upper = char.upper()
                if char_upper in all_chars:
                    self.morse_dict[char_upper] = all_chars[char_upper]
        else:
            # Use regular character sets
            self.morse_dict = {}
            if self.config['character_sets'].get('use_letters', False):
                self.morse_dict.update(self.morse_dict_letters)
            if self.config['character_sets'].get('use_numbers', False):
                self.morse_dict.update(self.morse_dict_numbers)
            if self.config['character_sets'].get('use_punctuation', False):
                self.morse_dict.update(self.morse_dict_punctuation)
        
        self.inverse_morse_dict = {v: k for k, v in self.morse_dict.items()}
        
        # Security: Thread management from config
        self.active_threads = []
        self.max_threads = self.config['security']['max_threads']
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.config['audio']['sample_rate'],
                                  output=True)
        
        # Load timing settings from config
        multiplier = self.config['timing']['multiplier']
        self.dit_duration = self.config['timing']['dit_duration_ratio'] * multiplier
        self.dah_duration = self.config['timing']['dah_duration_ratio'] * multiplier
        self.space_between_words = self.config['timing']['space_between_words_ratio'] * multiplier
        self.space_between_characters = self.config['timing']['space_between_characters_ratio'] * multiplier
        self.space_between_dit_dah = self.config['timing']['space_between_dit_dah_ratio'] * multiplier
        
        # Load audio settings
        self.audio_frequency = self.config['audio']['frequency']
        self.audio_volume = self.config['audio']['volume']

    def _load_config(self, config_file):
        """Load configuration from JSON file with validation."""
        try:
            # Sanitize config file path
            config_file = self._sanitize_config_path(config_file)
            if not config_file:
                logging.warning("Invalid config file path. Using defaults.")
                return self._get_default_config()
            
            # Try to load from current directory first
            if os.path.exists(config_file):
                config_path = config_file
            else:
                # Try to load from script directory
                script_dir = os.path.dirname(os.path.abspath(__file__))
                config_path = os.path.join(script_dir, config_file)
            
            if not os.path.exists(config_path):
                logging.warning(f"Configuration file not found: {config_file}. Using defaults.")
                return self._get_default_config()
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Validate config structure
            self._validate_config(config)
            logging.info(f"Configuration loaded from: {config_path}")
            return config
            
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in config file: {e}")
            return self._get_default_config()
        except ValueError as e:
            logging.error(f"Invalid config values: {e}")
            return self._get_default_config()
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _sanitize_config_path(self, file_path):
        """Sanitize configuration file path to prevent directory traversal attacks."""
        try:
            if not isinstance(file_path, str):
                return ""
            
            # Remove null bytes and control characters
            file_path = re.sub(r'[\x00-\x1F\x7F]', '', file_path)
            
            # Remove or escape dangerous patterns
            dangerous_patterns = [
                r'\.\./',  # Directory traversal
                r'\.\.\\', # Windows directory traversal
                r'\.\.',   # Any double dot
                r'[<>:"|?*]',  # Invalid filename characters
            ]
            
            for pattern in dangerous_patterns:
                file_path = re.sub(pattern, '', file_path)
            
            # Only allow specific file extensions
            allowed_extensions = ['.json', '.txt', '.cfg', '.config']
            if '.' in file_path:
                ext = '.' + file_path.split('.')[-1].lower()
                if ext not in allowed_extensions:
                    return ""
            else:
                # Default to .json if no extension
                file_path += '.json'
            
            # Limit path length
            if len(file_path) > 255:
                return ""
            
            return file_path.strip()
            
        except Exception:
            return ""

    def _get_default_config(self):
        """Return default configuration."""
        return {
            "audio": {
                "frequency": 600,
                "sample_rate": 44100,
                "volume": 1.0
            },
            "timing": {
                "multiplier": 0.06,
                "dit_duration_ratio": 1.2,
                "dah_duration_ratio": 2.5,
                "space_between_words_ratio": 4.0,
                "space_between_characters_ratio": 3.0,
                "space_between_dit_dah_ratio": 0.2,
                "round_delay": 0.5
            },
            "security": {
                "max_input_length": 1000,
                "max_threads": 5,
                "input_timeout": 30,
                "character_input_timeout": 60,
                "min_frequency": 50,
                "max_frequency": 5000,
                "min_duration": 0.001,
                "max_duration": 10.0,
                "max_rounds": 100,
                "max_sequence_length": 10
            },
            "game": {
                "default_rounds": 20,
                "default_sequence_length": 2
            },
            "character_sets": {
                "use_letters": True,
                "use_numbers": False,
                "use_punctuation": False
            }
        }

    def _validate_config(self, config):
        """Validate configuration structure and values."""
        required_sections = ['audio', 'timing', 'security', 'game', 'character_sets']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required config section: {section}")
        
        # Validate ranges
        audio = config['audio']
        if not (50 <= audio['frequency'] <= 5000):
            raise ValueError("Audio frequency must be between 50-5000 Hz")
        if not (8000 <= audio['sample_rate'] <= 96000):
            raise ValueError("Sample rate must be between 8000-96000 Hz")
        
        timing = config['timing']
        if timing['multiplier'] <= 0:
            raise ValueError("Timing multiplier must be positive")

    def to_morse(self, char):
        return self.morse_dict.get(char.upper(), '')

    def from_morse(self, morse_code):
        return self.inverse_morse_dict.get(morse_code, '')

    def play_tone(self, frequency, duration):
        # Security: Validate parameters using config values
        min_freq = self.config['security']['min_frequency']
        max_freq = self.config['security']['max_frequency']
        min_dur = self.config['security']['min_duration']
        max_dur = self.config['security']['max_duration']
        
        if not isinstance(frequency, (int, float)) or not (min_freq <= frequency <= max_freq):
            logging.warning(f"Invalid frequency attempted: {frequency}")
            raise ValueError(f"Frequency must be between {min_freq}-{max_freq} Hz")
        if not isinstance(duration, (int, float)) or not (min_dur <= duration <= max_dur):
            logging.warning(f"Invalid duration attempted: {duration}")
            raise ValueError(f"Duration must be between {min_dur}-{max_dur} seconds")
        
        volume = min(1.0, max(0.0, self.audio_volume))  # Clamp volume
        fs = 44100       # sampling rate, Hz, must be integer

        try:
            # generate samples, note conversion to float32 array
            samples = (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)

            # for paFloat32 sample values must be in range [-1.0, 1.0]
            self.stream.write((volume * samples).tobytes())
            time.sleep(duration)
        except Exception as e:
            logging.error(f"Audio playback error: {e}")
            raise

    def play_string(self, message):
        self.play_morse(self.string_to_morse(message))

    def play_morse(self, message):
        frequency = self.audio_frequency  # Frequency from config
        for char in message:
            if char == '.':
                self.play_tone(frequency, self.dit_duration)  # short beep
            elif char == '-':
                self.play_tone(frequency, self.dah_duration)  # long beep
            elif char == ' ':
                time.sleep(self.space_between_words)  # space between words
            elif char == '#':
                time.sleep(self.space_between_characters)  # space between characters
            time.sleep(self.space_between_dit_dah)  # space between characters

    def string_to_morse(self, input_string, max_length=None):
        # Security: Input validation and sanitization using config
        if max_length is None:
            max_length = self.config['security']['max_input_length']
        
        if not isinstance(input_string, str):
            logging.warning(f"Non-string input attempted: {type(input_string)}")
            raise TypeError("Input must be a string")
        
        if len(input_string) > max_length:
            logging.warning(f"Input too long attempted: {len(input_string)} characters")
            raise ValueError(f"Input too long. Maximum {max_length} characters allowed")
        
        # Sanitize input - only allow known characters and spaces
        sanitized = ''.join(c for c in input_string if c.upper() in self.morse_dict or c == ' ')
        if len(sanitized) != len(input_string):
            logging.info(f"Input sanitized: removed {len(input_string) - len(sanitized)} invalid characters")
        
        tmp = ''
        for char in sanitized:
            if char.upper() in self.morse_dict:
                tmp += self.to_morse(char) + '#'
            elif char == ' ':
                tmp += ' '
        return tmp

    def morse_to_string(self, morse_string):
        return ''.join(self.from_morse(code) for code in morse_string.split('#'))

    def __del__(self):
        # Security: Safe cleanup with error handling
        try:
            if hasattr(self, 'stream') and self.stream:
                self.stream.stop_stream()
                self.stream.close()
        except Exception as e:
            logging.error(f"Error closing audio stream: {e}")
        
        try:
            if hasattr(self, 'p') and self.p:
                self.p.terminate()
        except Exception as e:
            logging.error(f"Error terminating PyAudio: {e}")
        
        # Clean up any remaining threads
        try:
            if hasattr(self, 'active_threads'):
                for thread in self.active_threads:
                    if thread.is_alive():
                        thread.join(timeout=1.0)
        except Exception as e:
            logging.error(f"Error cleaning up threads: {e}")

    def getch(self, timeout=None):
        # Security: Add timeout and better error handling
        if timeout is None:
            timeout = self.config['security']['input_timeout']
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            # Add timeout to prevent indefinite blocking
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if ready:
                ch = sys.stdin.read(1)
                return ch
            else:
                logging.warning(f"Input timeout after {timeout} seconds")
                raise TimeoutError(f"Input timeout after {timeout} seconds")
        except Exception as e:
            logging.error(f"Terminal input error: {e}")
            raise
        finally:
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except Exception as e:
                logging.error(f"Failed to restore terminal settings: {e}")

    def play_random_and_verify(self, length=1):
        # Security: Validate length parameter using config
        max_length = self.config['security']['max_sequence_length']
        if not isinstance(length, int) or not (1 <= length <= max_length):
            logging.warning(f"Invalid length attempted: {length}")
            raise ValueError(f"Length must be between 1-{max_length} characters")
        
        # Security: Clean up old threads and check limits
        self.active_threads = [t for t in self.active_threads if t.is_alive()]
        if len(self.active_threads) >= self.max_threads:
            logging.warning(f"Too many active threads: {len(self.active_threads)}")
            raise RuntimeError(f"Too many active audio threads. Maximum {self.max_threads} allowed")
        
        try:
            chars = [random.choice(list(self.morse_dict.keys())) for _ in range(length)]
            random_string = ''.join(chars)
            morse_code = self.string_to_morse(random_string)
            
            # Security: Track thread
            thread = threading.Thread(target=self.play_morse, args=(morse_code,), daemon=True)
            self.active_threads.append(thread)
            thread.start()

            print(f"Enter the {length} character(s) you heard:")
            user_input = ''
            while len(user_input) < length:
                try:
                    char_timeout = self.config['security']['character_input_timeout']
                    char = self.getch(timeout=char_timeout).upper()
                    user_input += char
                except TimeoutError:
                    print("\nInput timeout. Skipping this round.")
                    return 0
                except KeyboardInterrupt:
                    print("\nInterrupted by user.")
                    return 0
                    
            if user_input == random_string:
                print("Correct!")
                return 1
            else:
                print(f"Incorrect. The correct answer was: {random_string}")
                return 0
        except Exception as e:
            logging.error(f"Error in play_random_and_verify: {e}")
            print(f"Error occurred: {e}")
            return 0

    def play_times(self, times, length=1):
        # Security: Validate parameters using config
        max_rounds = self.config['security']['max_rounds']
        max_length = self.config['security']['max_sequence_length']
        
        if not isinstance(times, int) or not (1 <= times <= max_rounds):
            logging.warning(f"Invalid times parameter: {times}")
            raise ValueError(f"Times must be between 1-{max_rounds}")
        if not isinstance(length, int) or not (1 <= length <= max_length):
            logging.warning(f"Invalid length parameter: {length}")
            raise ValueError(f"Length must be between 1-{max_length} characters")
        
        try:
            score = 0
            for i in range(times):
                try:
                    print(f"\nRound {i+1}/{times}")
                    score += self.play_random_and_verify(length)
                    # Delay between rounds from config
                    time.sleep(self.config['timing']['round_delay'])
                except KeyboardInterrupt:
                    print("\nGame interrupted by user.")
                    break
                except Exception as e:
                    logging.error(f"Error in round {i+1}: {e}")
                    print(f"Error in round {i+1}, skipping...")
                    continue
            
            print(f"\nFinal score: {score}/{times}")
            if times > 0:
                percentage = (score / times) * 100
                print(f"Accuracy: {percentage:.1f}%")
        except Exception as e:
            logging.error(f"Critical error in play_times: {e}")
            print(f"Critical error: {e}")

    def reload_config(self, config_file='config.json'):
        """Reload configuration from file and update settings."""
        try:
            self.config = self._load_config(config_file)
            
            # Update timing settings
            multiplier = self.config['timing']['multiplier']
            self.dit_duration = self.config['timing']['dit_duration_ratio'] * multiplier
            self.dah_duration = self.config['timing']['dah_duration_ratio'] * multiplier
            self.space_between_words = self.config['timing']['space_between_words_ratio'] * multiplier
            self.space_between_characters = self.config['timing']['space_between_characters_ratio'] * multiplier
            self.space_between_dit_dah = self.config['timing']['space_between_dit_dah_ratio'] * multiplier
            
            # Update audio settings
            self.audio_frequency = self.config['audio']['frequency']
            self.audio_volume = self.config['audio']['volume']
            
            # Update security settings
            self.max_threads = self.config['security']['max_threads']
            
            # Update character sets
            self.morse_dict = {}
            if self.config['character_sets']['use_letters']:
                self.morse_dict.update(self.morse_dict_letters)
            if self.config['character_sets']['use_numbers']:
                self.morse_dict.update(self.morse_dict_numbers)
            if self.config['character_sets']['use_punctuation']:
                self.morse_dict.update(self.morse_dict_punctuation)
            
            self.inverse_morse_dict = {v: k for k, v in self.morse_dict.items()}
            
            logging.info("Configuration reloaded successfully")
            print("Configuration reloaded from config.json")
            
        except Exception as e:
            logging.error(f"Error reloading config: {e}")
            print(f"Error reloading configuration: {e}")


# Example usage:
if __name__ == "__main__":
    # Create MorseCode instance with config file
    morse = MorseCode()
    
    # Use default values from config or override if needed
    default_rounds = morse.config['game']['default_rounds']
    default_length = morse.config['game']['default_sequence_length']
    
    print(f"Starting Morse Code practice: {default_rounds} rounds of {default_length}-character sequences")
    print("Configuration loaded from config.json")
    print(f"Using character sets: Letters={morse.config['character_sets']['use_letters']}, "
          f"Numbers={morse.config['character_sets']['use_numbers']}, "
          f"Punctuation={morse.config['character_sets']['use_punctuation']}")
    print("Press Ctrl+C to exit\n")
    
    try:
        morse.play_times(default_rounds, default_length)
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        logging.error(f"Application error: {e}")