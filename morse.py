import time
import pyaudio
import numpy as np
import random
import sys
import termios
import tty

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
    def __init__(self):
        self.morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
            '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--',
            '?': '..--..', '/': '-..-.'
        }
        self.inverse_morse_dict = {v: k for k, v in self.morse_dict.items()}
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  output=True)
        multiplier = 0.05
        self.dit_duration = 1.5 * multiplier
        self.dah_duration = 3.0 * multiplier
        self.space_between_words = 4.0 * multiplier
        self.space_between_characters = 3.0 * multiplier
        self.space_between_dit_dah = 0.1 * multiplier

    def to_morse(self, char):
        return self.morse_dict.get(char.upper(), '')

    def from_morse(self, morse_code):
        return self.inverse_morse_dict.get(morse_code, '')

    def play_tone(self, frequency, duration):
        volume = 1.0     # range [0.0, 1.0]
        fs = 44100       # sampling rate, Hz, must be integer

        # generate samples, note conversion to float32 array
        samples = (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        self.stream.write((volume * samples).tobytes())
        time.sleep(duration)

    def play_string(self, message):
        self.play_morse(morse.string_to_morse(message))

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

    def string_to_morse(self, input_string):
        #tmp = '#'.join(self.to_morse(char) for char in input_string if char.upper() in self.morse_dict)
        tmp = ''
        for char in input_string:
            if char.upper() in self.morse_dict:
                tmp += self.to_morse(char) + '#'
            elif char == ' ':
                tmp += ' '
        return tmp

    def morse_to_string(self, morse_string):
        return ''.join(self.from_morse(code) for code in morse_string.split('#'))

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    def play_random_and_verify(self):
        random_char = random.choice(list(self.morse_dict.keys()))
        morse_code = self.to_morse(random_char)
        self.play_morse(morse_code)
        
        #user_input = input("Enter the character you heard: ").upper()

        user_input = self.getch().upper()
        if user_input == random_char:
            print("Correct!")
            return 1
        else:
            print(f"Incorrect. The correct answer was: {random_char}")
            return 0
    
    def play_times(self, times):
        score = 0
        for _ in range(times):
            score += self.play_random_and_verify()
        print(f"Your score: {score}/{times}")

# Example usage:
morse = MorseCode()
morse.play_string('cq cq cq de HB9IKS K')  # Output: Morse code sound
#morse.play_times(20)