#!/usr/bin/env python3
"""
Morse Code Learning Application - GUI Version

A tkinter-based graphical interface for the Morse Code learning application.
Provides an easy-to-use window interface with practice area, configuration
controls, and real-time progress tracking.

Author: Generated with Claude Code
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import threading
import time
import os
from morse import MorseCode
import logging

class MorseCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Learning Application")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Set window icon if available
        try:
            # You could add an icon file here if you have one
            pass
        except Exception:
            pass
        
        # Make window visible and bring to front (with error handling for older tk)
        try:
            self.root.lift()
            if hasattr(self.root, 'attributes'):
                self.root.attributes('-topmost', True)
                self.root.after_idle(self.root.attributes, '-topmost', False)
        except (tk.TclError, AttributeError):
            # Fallback for older tkinter versions
            self.root.lift()
            try:
                self.root.focus_force()
            except tk.TclError:
                pass
        
        # Configure window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize Morse Code instance
        self.morse = None
        self.original_config = None
        
        try:
            self.morse = MorseCode()
            self.original_config = self.morse.config.copy()
        except Exception as e:
            # Create a minimal fallback config so GUI can still work
            self.original_config = {
                "audio": {"frequency": 600, "sample_rate": 44100, "volume": 1.0},
                "timing": {"multiplier": 0.06, "dit_duration_ratio": 1.2, "dah_duration_ratio": 2.5,
                          "space_between_words_ratio": 4.0, "space_between_characters_ratio": 3.0,
                          "space_between_dit_dah_ratio": 0.2, "round_delay": 0.5},
                "security": {"max_input_length": 1000, "max_threads": 5, "input_timeout": 30,
                           "character_input_timeout": 60, "min_frequency": 50, "max_frequency": 5000,
                           "min_duration": 0.001, "max_duration": 10.0, "max_rounds": 100, "max_sequence_length": 10},
                "game": {"default_rounds": 20, "default_sequence_length": 2},
                "character_sets": {"use_letters": True, "use_numbers": False, "use_punctuation": False}
            }
            # Show error but continue with GUI creation
            print(f"Warning: MorseCode initialization failed: {e}")
            print("GUI will continue with limited functionality")
        
        # GUI State variables
        self.current_sequence = ""
        self.user_input = ""
        self.current_round = 0
        self.total_rounds = 0
        self.correct_answers = 0
        self.practice_active = False
        self.audio_thread = None
        
        # Create GUI elements
        print("Creating GUI widgets...")
        self.create_widgets()
        print("Updating initial status...")
        self.update_status()
        print("GUI initialization complete")
        
        # Force window update and bring to front
        self.root.update_idletasks()
        self.root.update()
        
        # Try multiple methods to make window visible
        try:
            self.root.deiconify()  # Ensure window is not minimized
            self.root.lift()       # Bring to front
            self.root.focus_set()  # Give focus
        except Exception as e:
            print(f"Window management warning: {e}")
        
    def create_widgets(self):
        print("  → Creating style configuration...")
        # Create main notebook for tabs with style configuration
        style = ttk.Style()
        
        # Configure notebook style for better appearance
        try:
            # Try to set a modern theme if available
            available_themes = style.theme_names()
            if 'aqua' in available_themes:  # macOS
                style.theme_use('aqua')
            elif 'vista' in available_themes:  # Windows
                style.theme_use('vista')
            elif 'clam' in available_themes:  # Cross-platform modern
                style.theme_use('clam')
        except Exception:
            # Use default theme if modern ones aren't available
            pass
        
        print("  → Creating main notebook...")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        print("  → Creating Practice tab...")
        # Practice Tab
        self.practice_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.practice_frame, text="📚 Practice")
        self.create_practice_tab()
        
        print("  → Creating Configuration tab...")
        # Configuration Tab
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="⚙️ Configuration")
        self.create_config_tab()
        
        print("  → Creating Converter tab...")
        # Converter Tab
        self.converter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.converter_frame, text="🔄 Text Converter")
        self.create_converter_tab()
        
        print("  → All widgets created successfully!")
        
    def create_practice_tab(self):
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.practice_frame, text="Practice Settings")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Rounds and Length
        ttk.Label(settings_frame, text="Rounds:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.rounds_var = tk.IntVar(value=self.morse.config['game']['default_rounds'])
        self.rounds_spin = ttk.Spinbox(settings_frame, from_=1, to=100, textvariable=self.rounds_var, width=10)
        self.rounds_spin.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(settings_frame, text="Sequence Length:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.length_var = tk.IntVar(value=self.morse.config['game']['default_sequence_length'])
        self.length_spin = ttk.Spinbox(settings_frame, from_=1, to=10, textvariable=self.length_var, width=10)
        self.length_spin.grid(row=0, column=3, padx=5, pady=2)
        
        # Character Sets
        char_frame = ttk.Frame(settings_frame)
        char_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)
        
        self.use_letters_var = tk.BooleanVar(value=self.morse.config['character_sets']['use_letters'])
        self.use_numbers_var = tk.BooleanVar(value=self.morse.config['character_sets']['use_numbers'])
        self.use_punctuation_var = tk.BooleanVar(value=self.morse.config['character_sets']['use_punctuation'])
        
        ttk.Checkbutton(char_frame, text="Letters", variable=self.use_letters_var, 
                       command=self.update_character_sets).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(char_frame, text="Numbers", variable=self.use_numbers_var,
                       command=self.update_character_sets).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(char_frame, text="Punctuation", variable=self.use_punctuation_var,
                       command=self.update_character_sets).pack(side=tk.LEFT, padx=5)
        
        # Control Buttons
        control_frame = ttk.Frame(self.practice_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Practice", command=self.start_practice)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Practice", command=self.stop_practice, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.replay_button = ttk.Button(control_frame, text="Replay Audio", command=self.replay_audio, state=tk.DISABLED)
        self.replay_button.pack(side=tk.LEFT, padx=5)
        
        # Practice Area
        practice_area = ttk.LabelFrame(self.practice_frame, text="Practice Area")
        practice_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status Display
        self.status_var = tk.StringVar(value="Ready to start practice")
        self.status_label = ttk.Label(practice_area, textvariable=self.status_var, font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Input Area
        input_frame = ttk.Frame(practice_area)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Your Answer:", font=("Arial", 11)).pack()
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var, font=("Arial", 14, "bold"), 
                                   width=20, justify=tk.CENTER, state=tk.DISABLED)
        self.input_entry.pack(pady=5)
        self.input_entry.bind('<KeyRelease>', self.on_input_change)
        self.input_entry.bind('<Return>', self.submit_answer)
        
        # Progress Display
        progress_frame = ttk.LabelFrame(practice_area, text="Progress")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.StringVar(value="Round: 0/0 | Score: 0/0 (0%)")
        ttk.Label(progress_frame, textvariable=self.progress_var, font=("Arial", 11)).pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)
        
        # Results Display with better configuration
        self.results_text = scrolledtext.ScrolledText(
            practice_area, 
            height=8, 
            width=60,
            wrap=tk.WORD,
            font=('Courier', 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def create_config_tab(self):
        # Audio Configuration
        audio_frame = ttk.LabelFrame(self.config_frame, text="Audio Settings")
        audio_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(audio_frame, text="Frequency (Hz):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.freq_var = tk.IntVar(value=self.morse.config['audio']['frequency'])
        self.freq_spin = ttk.Spinbox(audio_frame, from_=50, to=5000, textvariable=self.freq_var, width=10)
        self.freq_spin.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(audio_frame, text="Volume:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.volume_var = tk.DoubleVar(value=self.morse.config['audio']['volume'])
        self.volume_scale = ttk.Scale(audio_frame, from_=0.0, to=1.0, variable=self.volume_var, orient=tk.HORIZONTAL)
        self.volume_scale.grid(row=0, column=3, padx=5, pady=2, sticky=tk.EW)
        
        # Timing Configuration
        timing_frame = ttk.LabelFrame(self.config_frame, text="Timing Settings")
        timing_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(timing_frame, text="Speed Multiplier:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.speed_var = tk.DoubleVar(value=self.morse.config['timing']['multiplier'])
        self.speed_scale = ttk.Scale(timing_frame, from_=0.01, to=0.2, variable=self.speed_var, orient=tk.HORIZONTAL)
        self.speed_scale.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)
        
        # Configuration Buttons
        config_buttons = ttk.Frame(self.config_frame)
        config_buttons.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(config_buttons, text="Apply Settings", command=self.apply_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_buttons, text="Reset to Defaults", command=self.reset_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_buttons, text="Load Config File", command=self.load_config_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_buttons, text="Save Config File", command=self.save_config_file).pack(side=tk.LEFT, padx=5)
        
        # Configuration Preview with better text widget
        preview_frame = ttk.LabelFrame(self.config_frame, text="Configuration Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.config_text = scrolledtext.ScrolledText(
            preview_frame, 
            height=15, 
            width=60,
            wrap=tk.NONE,
            font=('Courier', 9)
        )
        self.config_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.update_config_preview()
        
    def create_converter_tab(self):
        # Text to Morse
        text_to_morse_frame = ttk.LabelFrame(self.converter_frame, text="Text to Morse Code")
        text_to_morse_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(text_to_morse_frame, text="Enter text:").pack(anchor=tk.W, padx=5, pady=2)
        self.text_input = tk.Text(text_to_morse_frame, height=3, width=60)
        self.text_input.pack(fill=tk.X, padx=5, pady=2)
        
        button_frame1 = ttk.Frame(text_to_morse_frame)
        button_frame1.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame1, text="Convert to Morse", command=self.convert_to_morse).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame1, text="Play Morse Audio", command=self.play_morse_audio).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(text_to_morse_frame, text="Morse Code:").pack(anchor=tk.W, padx=5, pady=(10,2))
        self.morse_output = scrolledtext.ScrolledText(text_to_morse_frame, height=4, width=60)
        self.morse_output.pack(fill=tk.X, padx=5, pady=2)
        
        # Morse to Text with improved text areas
        morse_to_text_frame = ttk.LabelFrame(self.converter_frame, text="Morse Code to Text")
        morse_to_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(morse_to_text_frame, text="Enter Morse Code (use # between characters, space between words):").pack(anchor=tk.W, padx=5, pady=2)
        self.morse_input = scrolledtext.ScrolledText(
            morse_to_text_frame, 
            height=4, 
            width=60,
            wrap=tk.WORD,
            font=('Courier', 10)
        )
        self.morse_input.pack(fill=tk.X, padx=5, pady=2)
        
        button_frame2 = ttk.Frame(morse_to_text_frame)
        button_frame2.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame2, text="Convert to Text", command=self.convert_to_text).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(morse_to_text_frame, text="Text:").pack(anchor=tk.W, padx=5, pady=(10,2))
        self.text_output = tk.Text(
            morse_to_text_frame, 
            height=3, 
            width=60,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.text_output.pack(fill=tk.X, padx=5, pady=2)
        
    def update_character_sets(self):
        """Update the MorseCode instance with new character set selection"""
        try:
            # Update config
            self.morse.config['character_sets']['use_letters'] = self.use_letters_var.get()
            self.morse.config['character_sets']['use_numbers'] = self.use_numbers_var.get()
            self.morse.config['character_sets']['use_punctuation'] = self.use_punctuation_var.get()
            
            # Rebuild morse dictionary
            self.morse.morse_dict = {}
            if self.morse.config['character_sets']['use_letters']:
                self.morse.morse_dict.update(self.morse.morse_dict_letters)
            if self.morse.config['character_sets']['use_numbers']:
                self.morse.morse_dict.update(self.morse.morse_dict_numbers)
            if self.morse.config['character_sets']['use_punctuation']:
                self.morse.morse_dict.update(self.morse.morse_dict_punctuation)
            
            self.morse.inverse_morse_dict = {v: k for k, v in self.morse.morse_dict.items()}
            
            if not self.morse.morse_dict:
                messagebox.showwarning("Warning", "At least one character set must be selected!")
                self.use_letters_var.set(True)
                self.update_character_sets()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update character sets: {e}")
            
    def start_practice(self):
        """Start a practice session"""
        if not self.morse.morse_dict:
            messagebox.showwarning("Warning", "Please select at least one character set!")
            return
            
        try:
            self.total_rounds = self.rounds_var.get()
            self.sequence_length = self.length_var.get()
            self.current_round = 0
            self.correct_answers = 0
            self.practice_active = True
            
            # Update UI state
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.input_entry.config(state=tk.NORMAL)
            self.input_entry.focus()
            self.results_text.delete(1.0, tk.END)
            
            # Start first round
            self.next_round()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start practice: {e}")
            
    def stop_practice(self):
        """Stop the current practice session"""
        self.practice_active = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.replay_button.config(state=tk.DISABLED)
        self.input_entry.config(state=tk.DISABLED)
        self.input_var.set("")
        self.status_var.set("Practice stopped")
        
    def next_round(self):
        """Start the next round of practice"""
        if not self.practice_active or self.current_round >= self.total_rounds:
            self.finish_practice()
            return
            
        self.current_round += 1
        self.user_input = ""
        self.input_var.set("")
        
        # Generate random sequence
        import random
        chars = [random.choice(list(self.morse.morse_dict.keys())) for _ in range(self.sequence_length)]
        self.current_sequence = ''.join(chars)
        
        # Update status
        self.status_var.set(f"Round {self.current_round}/{self.total_rounds} - Listen carefully...")
        self.update_progress()
        
        # Play the sequence
        self.play_current_sequence()
        
    def play_current_sequence(self):
        """Play the current Morse sequence in a separate thread"""
        def play_audio():
            try:
                morse_code = self.morse.string_to_morse(self.current_sequence)
                self.morse.play_morse(morse_code)
                # Update UI after audio finishes
                self.root.after(0, self.audio_finished)
            except Exception as e:
                logging.error(f"Audio playback error: {e}")
                self.root.after(0, lambda: self.status_var.set("Audio error - check configuration"))
                
        self.replay_button.config(state=tk.DISABLED)
        self.audio_thread = threading.Thread(target=play_audio, daemon=True)
        self.audio_thread.start()
        
    def audio_finished(self):
        """Called when audio playback finishes"""
        if self.practice_active:
            self.status_var.set(f"Enter the {self.sequence_length} character(s) you heard:")
            self.replay_button.config(state=tk.NORMAL)
            self.input_entry.focus()
        
    def replay_audio(self):
        """Replay the current sequence"""
        if hasattr(self, 'current_sequence') and self.current_sequence:
            self.status_var.set("Replaying...")
            self.play_current_sequence()
            
    def on_input_change(self, event=None):
        """Handle input changes"""
        # event parameter is required by tkinter but not used
        del event  # Explicitly acknowledge unused parameter
        
        current_input = self.input_var.get().upper()
        
        # Auto-submit when enough characters entered
        if len(current_input) >= self.sequence_length and self.practice_active:
            self.root.after(100, self.submit_answer)  # Small delay for UI update
            
    def submit_answer(self, event=None):
        """Submit the current answer"""
        # event parameter is optional for Enter key binding
        del event  # Explicitly acknowledge unused parameter
        
        if not self.practice_active:
            return
            
        user_answer = self.input_var.get().upper()[:self.sequence_length]
        correct = user_answer == self.current_sequence
        
        if correct:
            self.correct_answers += 1
            result_text = f"Round {self.current_round}: ✓ Correct! ({self.current_sequence})\n"
            self.status_var.set("Correct! 🎉")
        else:
            result_text = f"Round {self.current_round}: ✗ Wrong. Answer: {self.current_sequence}, You: {user_answer}\n"
            self.status_var.set(f"Incorrect. The answer was: {self.current_sequence}")
            
        # Add to results
        self.results_text.insert(tk.END, result_text)
        self.results_text.see(tk.END)
        
        # Update progress
        self.update_progress()
        
        # Move to next round after a delay
        self.root.after(1500, self.next_round)
        
    def finish_practice(self):
        """Finish the practice session and show results"""
        self.practice_active = False
        percentage = (self.correct_answers / self.total_rounds * 100) if self.total_rounds > 0 else 0
        
        final_result = f"\n=== Practice Complete ===\n"
        final_result += f"Final Score: {self.correct_answers}/{self.total_rounds} ({percentage:.1f}%)\n"
        
        if percentage >= 90:
            final_result += "Excellent work! 🌟\n"
        elif percentage >= 75:
            final_result += "Great job! 👍\n"
        elif percentage >= 50:
            final_result += "Good progress! Keep practicing! 📚\n"
        else:
            final_result += "Keep practicing - you'll improve! 💪\n"
            
        self.results_text.insert(tk.END, final_result)
        self.results_text.see(tk.END)
        
        self.status_var.set(f"Practice complete! Score: {percentage:.1f}%")
        self.stop_practice()
        
    def update_progress(self):
        """Update the progress display"""
        if self.total_rounds > 0:
            percentage = (self.correct_answers / max(1, self.current_round - 1) * 100) if self.current_round > 1 else 0
            self.progress_var.set(f"Round: {self.current_round}/{self.total_rounds} | Score: {self.correct_answers}/{max(1, self.current_round - 1)} ({percentage:.1f}%)")
            self.progress_bar['maximum'] = self.total_rounds
            self.progress_bar['value'] = self.current_round
        
    def update_status(self):
        """Update the status display"""
        if self.morse and hasattr(self.morse, 'morse_dict'):
            char_count = len(self.morse.morse_dict)
            char_types = []
            if self.morse.config['character_sets']['use_letters']:
                char_types.append("Letters")
            if self.morse.config['character_sets']['use_numbers']:
                char_types.append("Numbers")
            if self.morse.config['character_sets']['use_punctuation']:
                char_types.append("Punctuation")
                
            status = f"Ready - {char_count} characters loaded ({', '.join(char_types)})"
        else:
            status = "⚠️ Audio unavailable - GUI demo mode (visual interface only)"
            
        self.status_var.set(status)
        
    def apply_config(self):
        """Apply configuration changes"""
        try:
            # Update audio settings
            self.morse.config['audio']['frequency'] = self.freq_var.get()
            self.morse.config['audio']['volume'] = self.volume_var.get()
            self.morse.audio_frequency = self.freq_var.get()
            self.morse.audio_volume = self.volume_var.get()
            
            # Update timing settings
            multiplier = self.speed_var.get()
            self.morse.config['timing']['multiplier'] = multiplier
            self.morse.dit_duration = self.morse.config['timing']['dit_duration_ratio'] * multiplier
            self.morse.dah_duration = self.morse.config['timing']['dah_duration_ratio'] * multiplier
            self.morse.space_between_words = self.morse.config['timing']['space_between_words_ratio'] * multiplier
            self.morse.space_between_characters = self.morse.config['timing']['space_between_characters_ratio'] * multiplier
            self.morse.space_between_dit_dah = self.morse.config['timing']['space_between_dit_dah_ratio'] * multiplier
            
            self.update_config_preview()
            messagebox.showinfo("Success", "Configuration applied successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply configuration: {e}")
            
    def reset_config(self):
        """Reset configuration to defaults"""
        try:
            self.morse.config = self.original_config.copy()
            
            # Reset GUI controls
            self.freq_var.set(self.morse.config['audio']['frequency'])
            self.volume_var.set(self.morse.config['audio']['volume'])
            self.speed_var.set(self.morse.config['timing']['multiplier'])
            
            self.apply_config()
            messagebox.showinfo("Success", "Configuration reset to defaults!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset configuration: {e}")
            
    def load_config_file(self):
        """Load configuration from file"""
        try:
            filename = filedialog.askopenfilename(
                title="Load Configuration File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                self.morse.reload_config(filename)
                
                # Update GUI controls
                self.freq_var.set(self.morse.config['audio']['frequency'])
                self.volume_var.set(self.morse.config['audio']['volume'])
                self.speed_var.set(self.morse.config['timing']['multiplier'])
                
                self.update_config_preview()
                messagebox.showinfo("Success", f"Configuration loaded from {os.path.basename(filename)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            
    def save_config_file(self):
        """Save current configuration to file"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Configuration File",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    json.dump(self.morse.config, f, indent=2)
                
                messagebox.showinfo("Success", f"Configuration saved to {os.path.basename(filename)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            
    def update_config_preview(self):
        """Update the configuration preview"""
        try:
            config_str = json.dumps(self.morse.config, indent=2)
            self.config_text.delete(1.0, tk.END)
            self.config_text.insert(1.0, config_str)
        except Exception as e:
            self.config_text.delete(1.0, tk.END)
            self.config_text.insert(1.0, f"Error displaying configuration: {e}")
            
    def convert_to_morse(self):
        """Convert text to Morse code"""
        try:
            text = self.text_input.get(1.0, tk.END).strip()
            if text:
                morse_code = self.morse.string_to_morse(text)
                self.morse_output.delete(1.0, tk.END)
                self.morse_output.insert(1.0, morse_code)
            else:
                messagebox.showwarning("Warning", "Please enter some text to convert!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert text: {e}")
            
    def play_morse_audio(self):
        """Play the Morse code audio"""
        try:
            morse_code = self.morse_output.get(1.0, tk.END).strip()
            if morse_code:
                def play_audio():
                    try:
                        self.morse.play_morse(morse_code)
                    except Exception as e:
                        logging.error(f"Audio playback error: {e}")
                        
                threading.Thread(target=play_audio, daemon=True).start()
            else:
                messagebox.showwarning("Warning", "No Morse code to play! Convert text first.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio: {e}")
            
    def convert_to_text(self):
        """Convert Morse code to text"""
        try:
            morse_code = self.morse_input.get(1.0, tk.END).strip()
            if morse_code:
                text = self.morse.morse_to_string(morse_code)
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(1.0, text)
            else:
                messagebox.showwarning("Warning", "Please enter Morse code to convert!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert Morse code: {e}")

    def on_closing(self):
        """Handle window closing"""
        try:
            # Stop any active practice
            if self.practice_active:
                self.stop_practice()
            
            # Clean up audio resources
            if hasattr(self, 'morse') and self.morse:
                try:
                    self.morse.__del__()
                except:
                    pass
            
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            self.root.quit()


def main():
    """Main function to run the GUI application"""
    try:
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - GUI - %(message)s')
        
        print("Starting Morse Code GUI Application...")
        
        # Check tkinter availability
        try:
            import tkinter as tk
            print(f"Using tkinter version: {tk.TkVersion} (Tcl: {tk.TclVersion})")
        except ImportError:
            print("Error: tkinter is not available. Please install tkinter.")
            return 1
        
        # Create the main window
        print("Creating main window...")
        root = tk.Tk()
        
        # Set up better error handling for the root window
        root.report_callback_exception = lambda exc_type, exc_value, exc_traceback: (
            print(f"GUI Error: {exc_type.__name__}: {exc_value}"),
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        )
        
        # Create the application
        print("Initializing GUI components...")
        app = MorseCodeGUI(root)
        
        # Ensure app is referenced to avoid warnings
        if not app:
            raise RuntimeError("Failed to create GUI application")
        
        print("GUI ready! Window should now be visible.")
        print("Close the window or press Ctrl+C to exit.")
        
        # Start the GUI event loop
        root.mainloop()
        
        print("GUI application closed.")
        return 0
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 0
    except Exception as e:
        print(f"Failed to start GUI application: {e}")
        import traceback
        traceback.print_exc()
        
        # Additional troubleshooting info
        print("\nTroubleshooting:")
        print("1. Ensure you have a display available (not running headless)")
        print("2. Try running: python test_gui.py for basic testing")
        print("3. Check that tkinter is properly installed")
        print("4. On Linux, you may need: sudo apt-get install python3-tk")
        
        return 1


if __name__ == "__main__":
    main()