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
            ':': '---...', '=': '-...-', '?': '..--..'
        }
        self.inverse_morse_dict = {v: k for k, v in self.morse_dict.items()}
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  output=True)

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
        for char in message:
            if char == '.':
                self.play_tone(1000, 0.1)  # short beep
            elif char == '-':
                self.play_tone(1000, 0.3)  # long beep
            elif char == ' ':
                time.sleep(0.4)  # space between words
            time.sleep(0.1)  # space between characters

    def string_to_morse(self, input_string):
        return ' '.join(self.to_morse(char) for char in input_string if char.upper() in self.morse_dict)

    def morse_to_string(self, morse_string):
        return ''.join(self.from_morse(code) for code in morse_string.split(' '))

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

# Example usage:
morse = MorseCode()
print(morse.to_morse('A'))  # Output: .-
print(morse.from_morse('.-'))  # Output: A
morse.play_morse(morse.string_to_morse('hello world'))  # Output: Morse code sound