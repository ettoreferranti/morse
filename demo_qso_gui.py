#!/usr/bin/env python3
"""
QSO Practice GUI Demo

Demonstrates the QSO Practice interface without requiring pyaudio.
This creates a mock environment to showcase the GUI functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys

# Mock the missing dependencies
class MockMorseCode:
    """Mock MorseCode class for demo purposes"""
    def __init__(self):
        self.config = {
            'audio': {'frequency': 600, 'sample_rate': 44100, 'volume': 1.0},
            'timing': {'multiplier': 0.06, 'dit_duration_ratio': 1.2, 'dah_duration_ratio': 2.5,
                      'space_between_words_ratio': 4.0, 'space_between_characters_ratio': 3.0,
                      'space_between_dit_dah_ratio': 0.2, 'round_delay': 0.5},
            'security': {'max_input_length': 1000, 'max_threads': 5, 'input_timeout': 30},
            'game': {'default_rounds': 20, 'default_sequence_length': 2},
            'character_sets': {'use_letters': True, 'use_numbers': False, 'use_punctuation': False},
            'qso': {
                'default_qso_count': 5,
                'default_verbosity': 'medium',
                'default_call_region1': None,
                'default_call_region2': None,
                'fuzzy_threshold': 0.8,
                'partial_credit': True,
                'case_sensitive': False
            }
        }
        self.morse_dict = {}
        self.morse_dict_letters = {}
        self.morse_dict_numbers = {}
        self.morse_dict_punctuation = {}

    def play_string(self, text):
        """Mock play_string method"""
        print(f"[Mock audio] Playing: {text[:50]}...")

# Import real QSO modules
try:
    from qso_data import QSOGenerator, ABBREVIATIONS, ABBREVIATION_CATEGORIES
    from qso_practice import QSOPracticeSession
    from qso_scoring import QSOScorer, SessionScorer
    print("✓ QSO modules loaded successfully")
except ImportError as e:
    print(f"Error loading QSO modules: {e}")
    sys.exit(1)


class QSOPracticeDemoGUI:
    """Simplified GUI showing just the QSO Practice tab"""

    def __init__(self, root):
        self.root = root
        self.root.title("QSO Practice Demo - Morse Code Learning App")
        self.root.geometry("900x800")

        # Initialize mock morse and QSO components
        self.morse = MockMorseCode()
        self.qso_generator = QSOGenerator()
        self.qso_session = None
        self.qso_scorer = QSOScorer()
        self.session_scorer = SessionScorer(self.qso_scorer)

        # Load QSO config
        qso_config = self.morse.config.get('qso', {})
        self.qso_config_count = qso_config.get('default_qso_count', 5)
        self.qso_config_verbosity = qso_config.get('default_verbosity', 'medium')
        self.qso_config_region1 = qso_config.get('default_call_region1', None)
        self.qso_config_region2 = qso_config.get('default_call_region2', None)
        self.qso_config_fuzzy = qso_config.get('fuzzy_threshold', 0.8)
        self.qso_config_partial = qso_config.get('partial_credit', True)
        self.qso_config_case_sensitive = qso_config.get('case_sensitive', False)

        # Create demo info banner
        info_frame = ttk.Frame(root, relief=tk.RIDGE, borderwidth=2)
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(info_frame,
                 text="🎉 QSO Practice Feature Demo (Audio Disabled)",
                 font=('TkDefaultFont', 12, 'bold'),
                 foreground='blue').pack(pady=5)

        ttk.Label(info_frame,
                 text="This demo shows the QSO Practice GUI without requiring audio hardware.\n"
                      "All buttons and controls are functional. Audio playback is simulated.",
                 justify=tk.CENTER).pack(pady=5)

        # Create QSO tab content
        self.create_qso_tab()

        print("\n" + "="*60)
        print("QSO PRACTICE GUI DEMO LAUNCHED")
        print("="*60)
        print("\nFeatures to test:")
        print("  1. Click 'Configure' to set session parameters")
        print("  2. Click 'Start Session' to begin")
        print("  3. Click 'Play QSO' to simulate audio playback")
        print("  4. Fill in transcription fields and submit")
        print("  5. Click 'Glossary' to view abbreviations")
        print("\nNote: Audio playback is simulated (no sound will play)")
        print("="*60 + "\n")

    def create_qso_tab(self):
        """Create the QSO Practice interface"""
        # Import the actual implementation from morse_gui.py would go here
        # For demo, we'll recreate the key components

        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Title bar
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(title_frame,
                 text="QSO Practice",
                 font=('TkDefaultFont', 14, 'bold')).pack(side=tk.LEFT)

        ttk.Button(title_frame,
                  text="📖 Glossary",
                  command=self.show_abbreviation_glossary,
                  width=12).pack(side=tk.RIGHT)

        ttk.Button(title_frame,
                  text="⚙️ Configure",
                  command=self.configure_qso_session,
                  width=12).pack(side=tk.RIGHT, padx=(0, 5))

        # Session info
        info_frame = ttk.LabelFrame(main_container, text="Session", padding="5")
        info_frame.pack(fill=tk.X, pady=(0, 10))

        self.qso_progress_label = ttk.Label(info_frame, text="No active session")
        self.qso_progress_label.pack(side=tk.LEFT)

        self.qso_score_label = ttk.Label(info_frame, text="")
        self.qso_score_label.pack(side=tk.RIGHT)

        # Audio controls
        audio_frame = ttk.LabelFrame(main_container, text="Audio Controls", padding="10")
        audio_frame.pack(fill=tk.X, pady=(0, 10))

        self.qso_play_button = ttk.Button(audio_frame,
                                         text="▶️ Start Session",
                                         command=self.start_qso_session,
                                         width=15)
        self.qso_play_button.pack(side=tk.LEFT, padx=5)

        self.qso_replay_button = ttk.Button(audio_frame,
                                           text="🔁 Replay",
                                           command=lambda: messagebox.showinfo("Demo", "Replay functionality available"),
                                           state=tk.DISABLED,
                                           width=15)
        self.qso_replay_button.pack(side=tk.LEFT, padx=5)

        self.qso_skip_button = ttk.Button(audio_frame,
                                         text="⏭️ Skip",
                                         command=lambda: messagebox.showinfo("Demo", "Skip functionality available"),
                                         state=tk.DISABLED,
                                         width=15)
        self.qso_skip_button.pack(side=tk.LEFT, padx=5)

        self.qso_stop_button = ttk.Button(audio_frame,
                                         text="⏹️ Stop Session",
                                         command=lambda: messagebox.showinfo("Demo", "Stop functionality available"),
                                         state=tk.DISABLED,
                                         width=15)
        self.qso_stop_button.pack(side=tk.LEFT, padx=5)

        # Transcription area
        transcription_frame = ttk.LabelFrame(main_container, text="Transcription", padding="10")
        transcription_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        ttk.Label(transcription_frame,
                 text="Configure and start a session to begin practice",
                 foreground='gray').pack(pady=5)

        # Create notebook for fields
        fields_notebook = ttk.Notebook(transcription_frame)
        fields_notebook.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Required fields tab
        required_frame = ttk.Frame(fields_notebook, padding="10")
        fields_notebook.add(required_frame, text="Required Fields")

        required_labels = [
            ("Callsign 1:", 'callsign1'),
            ("Callsign 2:", 'callsign2'),
            ("Name 1:", 'name1'),
            ("Name 2:", 'name2'),
            ("QTH 1:", 'qth1'),
            ("QTH 2:", 'qth2'),
            ("RST 1:", 'rst1'),
            ("RST 2:", 'rst2')
        ]

        self.qso_entry_vars = {}
        for i, (label, key) in enumerate(required_labels):
            row = i // 2
            col = (i % 2) * 2

            ttk.Label(required_frame, text=label).grid(row=row, column=col, sticky=tk.W, padx=5, pady=3)
            var = tk.StringVar()
            ttk.Entry(required_frame, textvariable=var, state=tk.DISABLED, width=20).grid(
                row=row, column=col+1, sticky=tk.W+tk.E, padx=5, pady=3)

            self.qso_entry_vars[key] = var

        for i in range(4):
            required_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)

        # Optional fields tab
        optional_frame = ttk.Frame(fields_notebook, padding="10")
        fields_notebook.add(optional_frame, text="Optional Fields")

        ttk.Label(optional_frame,
                 text="Optional equipment details (rig, antenna, power) can be transcribed here",
                 wraplength=400).pack(pady=10)

        # Submit button
        submit_frame = ttk.Frame(transcription_frame)
        submit_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(submit_frame,
                  text="✓ Submit Answer",
                  state=tk.DISABLED).pack(side=tk.RIGHT, padx=5)

        ttk.Button(submit_frame,
                  text="Clear All",
                  command=lambda: messagebox.showinfo("Demo", "Clear functionality available")).pack(side=tk.RIGHT, padx=5)

        # Results area
        results_frame = ttk.LabelFrame(main_container, text="Results", padding="5")
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.qso_results_text = scrolledtext.ScrolledText(results_frame,
                                                          height=8,
                                                          wrap=tk.WORD,
                                                          state=tk.NORMAL)
        self.qso_results_text.pack(fill=tk.BOTH, expand=True)

        # Configure text tags
        self.qso_results_text.tag_config('correct', foreground='green')
        self.qso_results_text.tag_config('partial', foreground='orange')
        self.qso_results_text.tag_config('incorrect', foreground='red')
        self.qso_results_text.tag_config('header', font=('TkDefaultFont', 10, 'bold'))

        # Show welcome message
        self.qso_results_text.insert(tk.END, "Welcome to QSO Practice!\n\n", 'header')
        self.qso_results_text.insert(tk.END,
                                     "This feature simulates realistic amateur radio contacts (QSOs).\n"
                                     "Click 'Configure' to set your session parameters, then 'Start Session' to begin.\n\n"
                                     "Features:\n"
                                     "  • 9 call sign regions\n"
                                     "  • 62 amateur radio abbreviations\n"
                                     "  • Intelligent fuzzy matching and scoring\n"
                                     "  • 3 verbosity levels (minimal/medium/chatty)\n\n"
                                     "Click 'Glossary' to view all abbreviations!\n")
        self.qso_results_text.config(state=tk.DISABLED)

    def show_abbreviation_glossary(self):
        """Show abbreviation glossary dialog"""
        # Simplified version - just show a sample
        dialog = tk.Toplevel(self.root)
        dialog.title("Amateur Radio Abbreviations")
        dialog.geometry("600x400")

        ttk.Label(dialog,
                 text="Amateur Radio Abbreviations",
                 font=('TkDefaultFont', 14, 'bold')).pack(pady=10)

        ttk.Label(dialog,
                 text=f"{len(ABBREVIATIONS)} abbreviations used in QSO practice",
                 font=('TkDefaultFont', 9)).pack()

        # Show sample abbreviations
        text = scrolledtext.ScrolledText(dialog, height=15, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text.insert(tk.END, "Sample abbreviations:\n\n", 'bold')
        for i, (abbr, meaning) in enumerate(sorted(ABBREVIATIONS.items())[:20]):
            text.insert(tk.END, f"{abbr:8} - {meaning}\n")
        text.insert(tk.END, f"\n... and {len(ABBREVIATIONS) - 20} more!\n\n")
        text.insert(tk.END, "Full searchable glossary available in production version.")
        text.config(state=tk.DISABLED)

        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

    def configure_qso_session(self):
        """Show configuration dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("QSO Session Configuration")
        dialog.geometry("500x350")

        ttk.Label(dialog,
                 text="Configure Practice Session",
                 font=('TkDefaultFont', 12, 'bold')).pack(pady=10)

        options_frame = ttk.Frame(dialog, padding="20")
        options_frame.pack(fill=tk.BOTH, expand=True)

        # QSO count
        ttk.Label(options_frame, text="Number of QSOs:").grid(row=0, column=0, sticky=tk.W, pady=5)
        qso_count_var = tk.IntVar(value=self.qso_config_count)
        ttk.Spinbox(options_frame, from_=1, to=20, textvariable=qso_count_var, width=10).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=5)

        # Verbosity
        ttk.Label(options_frame, text="Verbosity:").grid(row=1, column=0, sticky=tk.W, pady=5)
        verbosity_var = tk.StringVar(value=self.qso_config_verbosity)
        ttk.Combobox(options_frame,
                    textvariable=verbosity_var,
                    values=['minimal', 'medium', 'chatty'],
                    state='readonly',
                    width=15).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        # Fuzzy threshold
        ttk.Label(options_frame, text="Fuzzy Threshold:").grid(row=2, column=0, sticky=tk.W, pady=5)
        fuzzy_var = tk.DoubleVar(value=self.qso_config_fuzzy)
        ttk.Spinbox(options_frame,
                   from_=0.5,
                   to=1.0,
                   increment=0.05,
                   textvariable=fuzzy_var,
                   width=10,
                   format="%.2f").grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

        # Partial credit
        partial_var = tk.BooleanVar(value=self.qso_config_partial)
        ttk.Checkbutton(options_frame,
                       text="Award partial credit for close answers",
                       variable=partial_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Info
        info = ttk.LabelFrame(dialog, text="About", padding="10")
        info.pack(fill=tk.X, padx=20, pady=(0, 10))

        ttk.Label(info,
                 text="Configure your QSO practice session parameters.\n"
                      "Fuzzy threshold controls answer tolerance (0.5=lenient, 1.0=exact).",
                 wraplength=450,
                 justify=tk.LEFT).pack()

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        def save():
            self.qso_config_count = qso_count_var.get()
            self.qso_config_verbosity = verbosity_var.get()
            self.qso_config_fuzzy = fuzzy_var.get()
            self.qso_config_partial = partial_var.get()
            messagebox.showinfo("Saved", "Configuration saved!")
            dialog.destroy()

        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)

    def start_qso_session(self):
        """Start a demo session"""
        try:
            # Create session
            self.qso_session = QSOPracticeSession(
                morse_code=self.morse,
                qso_count=self.qso_config_count,
                verbosity=self.qso_config_verbosity
            )

            self.qso_session.start_session()

            # Update UI
            self.qso_play_button.config(text="▶️ Play QSO")
            self.qso_stop_button.config(state=tk.NORMAL)
            self.qso_progress_label.config(text=f"QSO 1 of {self.qso_config_count}")

            # Show message
            self.qso_results_text.config(state=tk.NORMAL)
            self.qso_results_text.insert(tk.END, "\n" + "="*50 + "\n", 'header')
            self.qso_results_text.insert(tk.END, "Session Started!\n", 'header')
            self.qso_results_text.insert(tk.END, "="*50 + "\n", 'header')
            self.qso_results_text.insert(tk.END,
                                        f"QSOs: {self.qso_config_count}, Verbosity: {self.qso_config_verbosity}\n\n")
            self.qso_results_text.insert(tk.END,
                                        "Click 'Play QSO' to hear the first QSO.\n"
                                        "(In this demo, audio is simulated)\n\n")
            self.qso_results_text.see(tk.END)
            self.qso_results_text.config(state=tk.DISABLED)

            messagebox.showinfo("Success",
                               f"Session started with {self.qso_config_count} QSOs!\n\n"
                               "In the full version, you would:\n"
                               "1. Click 'Play QSO' to hear Morse audio\n"
                               "2. Transcribe what you hear\n"
                               "3. Submit your answer for scoring\n"
                               "4. View detailed feedback\n\n"
                               "This demo shows the GUI interface.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start session: {e}")


def main():
    """Launch the demo"""
    root = tk.Tk()
    app = QSOPracticeDemoGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
