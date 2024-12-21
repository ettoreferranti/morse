import time
import pyaudio
import numpy as np

class MorseCode:
    def __init__(self):
        self.morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
            '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--',
            ':': '---...', '=': '-...-', '?': '..--..', ' ': ' '
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
        tmp = '#'.join(self.to_morse(char) for char in input_string if char.upper() in self.morse_dict)
        return tmp

    def morse_to_string(self, morse_string):
        return ''.join(self.from_morse(code) for code in morse_string.split('#'))

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

# Example usage:
morse = MorseCode()
morse.play_morse(morse.string_to_morse('cq cq cq de HB9IKS'))  # Output: Morse code sound