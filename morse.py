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
    """
    def __init__(self, use_letters=True, use_numbers=True, use_punctuation=True):
        # Setup security logging
        logging.basicConfig(level=logging.WARNING, format='%(asctime)s - SECURITY - %(message)s')
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

        # Select which dictionaries to include
        self.morse_dict = {}
        if use_letters:
            self.morse_dict.update(self.morse_dict_letters)
        if use_numbers:
            self.morse_dict.update(self.morse_dict_numbers)
        if use_punctuation:
            self.morse_dict.update(self.morse_dict_punctuation)
        
        self.inverse_morse_dict = {v: k for k, v in self.morse_dict.items()}
        
        # Security: Thread management
        self.active_threads = []
        self.max_threads = 5
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  output=True)
        multiplier = 0.06
        self.dit_duration = 1.2 * multiplier
        self.dah_duration = 2.5 * multiplier
        self.space_between_words = 4.0 * multiplier
        self.space_between_characters = 3.0 * multiplier
        self.space_between_dit_dah = 0.2 * multiplier

    def to_morse(self, char):
        return self.morse_dict.get(char.upper(), '')

    def from_morse(self, morse_code):
        return self.inverse_morse_dict.get(morse_code, '')

    def play_tone(self, frequency, duration):
        # Security: Validate parameters to prevent resource exhaustion
        if not isinstance(frequency, (int, float)) or not (50 <= frequency <= 5000):
            logging.warning(f"Invalid frequency attempted: {frequency}")
            raise ValueError("Frequency must be between 50-5000 Hz")
        if not isinstance(duration, (int, float)) or not (0.001 <= duration <= 10.0):
            logging.warning(f"Invalid duration attempted: {duration}")
            raise ValueError("Duration must be between 0.001-10 seconds")
        
        volume = min(1.0, max(0.0, 1.0))  # Clamp volume
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
        frequency = 600  # Frequency in Hz
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

    def string_to_morse(self, input_string, max_length=1000):
        # Security: Input validation and sanitization
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

    def getch(self, timeout=30):
        # Security: Add timeout and better error handling
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
        # Security: Validate length parameter
        if not isinstance(length, int) or not (1 <= length <= 10):
            logging.warning(f"Invalid length attempted: {length}")
            raise ValueError("Length must be between 1-10 characters")
        
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
                    char = self.getch(timeout=60).upper()  # 60 second timeout per character
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
        # Security: Validate parameters
        if not isinstance(times, int) or not (1 <= times <= 100):
            logging.warning(f"Invalid times parameter: {times}")
            raise ValueError("Times must be between 1-100")
        if not isinstance(length, int) or not (1 <= length <= 10):
            logging.warning(f"Invalid length parameter: {length}")
            raise ValueError("Length must be between 1-10 characters")
        
        try:
            score = 0
            for i in range(times):
                try:
                    print(f"\nRound {i+1}/{times}")
                    score += self.play_random_and_verify(length)
                    # Small delay between rounds to prevent resource exhaustion
                    time.sleep(0.5)
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


# Example usage:
morse = MorseCode(use_letters=True, use_numbers=False, use_punctuation=False)
morse.play_times(20, 2)  # Play random Morse code sequences and verify user inputs