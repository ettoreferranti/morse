"""
QSO Practice Session Manager

Coordinates QSO generation, audio playback, and user interaction for
practice sessions. Integrates QSOGenerator with MorseCode audio engine.

Author: Generated with Claude Code
Date: 2025-11-28
Issue: #6 - QSO Feature: Practice Session Manager
Version: 1.0.0
"""

import threading
import time
from typing import Dict, List, Optional, Literal, Callable
from qso_data import QSOGenerator


# Type aliases for clarity
SessionState = Literal['ready', 'playing', 'transcribing', 'complete', 'paused', 'stopped']
VerbosityLevel = Literal['minimal', 'medium', 'chatty']


class QSOPracticeSession:
    """
    Manages a practice session with multiple QSOs.

    Coordinates QSO generation, audio playback via MorseCode class,
    session state management, and progress tracking.

    Session states:
    - ready: Session initialized, ready to start
    - playing: Currently playing QSO audio
    - transcribing: User is transcribing the QSO
    - complete: Session finished
    - paused: Session paused mid-playback
    - stopped: Session stopped by user

    Example usage:
        from morse import MorseCode

        morse_code = MorseCode()
        session = QSOPracticeSession(
            morse_code=morse_code,
            qso_count=5,
            verbosity='medium'
        )

        session.start_session()
        session.play_current_qso()
        # User transcribes...
        session.next_qso()
    """

    def __init__(
        self,
        morse_code,  # MorseCode instance for audio playback
        qso_count: int = 5,
        verbosity: VerbosityLevel = 'medium',
        call_region1: Optional[str] = None,
        call_region2: Optional[str] = None,
        seed: Optional[int] = None
    ):
        """
        Initialize a QSO practice session.

        Args:
            morse_code: MorseCode instance for audio playback
            qso_count: Number of QSOs in this session (1-100)
            verbosity: QSO verbosity level ('minimal', 'medium', 'chatty')
            call_region1: Optional region for first call sign
            call_region2: Optional region for second call sign
            seed: Optional random seed for reproducibility

        Raises:
            ValueError: If qso_count is out of range (1-100)
            ValueError: If verbosity is not valid
        """
        # Validate inputs
        if not isinstance(qso_count, int) or qso_count < 1 or qso_count > 100:
            raise ValueError("qso_count must be an integer between 1 and 100")

        if verbosity not in ('minimal', 'medium', 'chatty'):
            raise ValueError("verbosity must be 'minimal', 'medium', or 'chatty'")

        # Store configuration
        self.morse_code = morse_code
        self.qso_count = qso_count
        self.verbosity = verbosity
        self.call_region1 = call_region1
        self.call_region2 = call_region2
        self.seed = seed

        # Initialize QSO generator
        self.qso_generator = QSOGenerator(seed=seed)

        # Session state
        self.state: SessionState = 'ready'
        self.current_qso_index = 0
        self.qsos: List[Dict] = []
        self.current_qso: Optional[Dict] = None

        # Audio playback control
        self._playback_thread: Optional[threading.Thread] = None
        self._playback_complete = threading.Event()
        self._stop_playback = threading.Event()
        self._pause_playback = threading.Event()

        # Progress tracking
        self.qsos_completed = 0
        self.total_qsos_played = 0

        # Callbacks for event notifications (GUI integration)
        self._on_state_change: Optional[Callable[[SessionState], None]] = None
        self._on_progress_update: Optional[Callable[[int, int], None]] = None
        self._on_playback_complete: Optional[Callable[[], None]] = None

    def set_state_change_callback(self, callback: Callable[[SessionState], None]):
        """Set callback for state change events."""
        self._on_state_change = callback

    def set_progress_update_callback(self, callback: Callable[[int, int], None]):
        """Set callback for progress updates (current, total)."""
        self._on_progress_update = callback

    def set_playback_complete_callback(self, callback: Callable[[], None]):
        """Set callback for playback completion."""
        self._on_playback_complete = callback

    def _update_state(self, new_state: SessionState):
        """Update session state and trigger callback."""
        self.state = new_state
        if self._on_state_change:
            self._on_state_change(new_state)

    def _update_progress(self):
        """Update progress and trigger callback."""
        if self._on_progress_update:
            self._on_progress_update(self.current_qso_index + 1, self.qso_count)

    def start_session(self):
        """
        Start a new practice session.

        Generates all QSOs for the session and transitions to 'ready' state.

        Raises:
            RuntimeError: If session is already in progress
        """
        if self.state not in ('ready', 'complete', 'stopped'):
            raise RuntimeError(f"Cannot start session in state: {self.state}")

        # Generate all QSOs for the session
        # If call regions are specified, generate individually
        if self.call_region1 or self.call_region2:
            self.qsos = [
                self.qso_generator.generate_qso(
                    verbosity=self.verbosity,
                    call_region1=self.call_region1,
                    call_region2=self.call_region2
                )
                for _ in range(self.qso_count)
            ]
        else:
            # Use batch generation for efficiency
            self.qsos = self.qso_generator.generate_multiple_qsos(
                count=self.qso_count,
                verbosity=self.verbosity
            )

        # Reset session state
        self.current_qso_index = 0
        self.qsos_completed = 0
        self.total_qsos_played = 0
        self.current_qso = self.qsos[0]

        self._update_state('ready')
        self._update_progress()

    def play_current_qso(self):
        """
        Play the current QSO audio.

        Plays the Morse code audio for the current QSO in a separate thread
        to avoid blocking. Updates state to 'playing' during playback and
        'transcribing' when complete.

        Raises:
            RuntimeError: If no session is active or not in valid state
        """
        if not self.qsos:
            raise RuntimeError("No active session. Call start_session() first")

        if self.state not in ('ready', 'transcribing', 'paused'):
            raise RuntimeError(f"Cannot play QSO in state: {self.state}")

        if self.current_qso_index >= len(self.qsos):
            raise RuntimeError("No more QSOs to play")

        # Reset playback control flags
        self._playback_complete.clear()
        self._stop_playback.clear()
        self._pause_playback.clear()

        # Update state
        self._update_state('playing')

        # Start playback in separate thread
        self._playback_thread = threading.Thread(
            target=self._play_qso_thread,
            daemon=True
        )
        self._playback_thread.start()

    def _play_qso_thread(self):
        """Thread function for QSO audio playback."""
        try:
            # Get Morse text for current QSO
            morse_text = self.qso_generator.get_morse_text(self.current_qso)

            # Set the stop and pause events for the morse code player
            self.morse_code.stop_event = self._stop_playback
            self.morse_code.pause_event = self._pause_playback

            # Play the Morse code
            # Note: MorseCode.play_string() handles the actual audio playback
            self.morse_code.play_string(morse_text)

            # Clean up the event references
            self.morse_code.stop_event = None
            self.morse_code.pause_event = None

            # Mark playback as complete if not stopped
            if not self._stop_playback.is_set():
                self._playback_complete.set()
                self.total_qsos_played += 1

                # Update state to transcribing
                self._update_state('transcribing')

                # Trigger callback
                if self._on_playback_complete:
                    self._on_playback_complete()

        except Exception as e:
            # Log error and update state
            print(f"Error during QSO playback: {e}")
            self._update_state('stopped')

    def replay_current_qso(self):
        """
        Replay the current QSO audio.

        Allows user to hear the QSO again for better comprehension.

        Raises:
            RuntimeError: If not in transcribing state
        """
        if self.state != 'transcribing':
            raise RuntimeError("Can only replay in transcribing state")

        # Play again
        self.play_current_qso()

    def pause_playback(self):
        """
        Pause the current playback.

        Note: Current implementation stops playback. Full pause/resume
        would require deeper integration with MorseCode class.

        Raises:
            RuntimeError: If not currently playing
        """
        if self.state != 'playing':
            raise RuntimeError("Can only pause during playback")

        self._pause_playback.set()
        self._update_state('paused')

    def resume_playback(self):
        """
        Resume paused playback.

        Raises:
            RuntimeError: If not currently paused
        """
        if self.state != 'paused':
            raise RuntimeError("Can only resume from paused state")

        self._pause_playback.clear()
        self._update_state('playing')

    def stop_playback(self):
        """
        Stop the current playback.

        Raises:
            RuntimeError: If not currently playing
        """
        if self.state not in ('playing', 'paused'):
            raise RuntimeError("Can only stop during playback or when paused")

        self._stop_playback.set()
        self._update_state('stopped')

    def next_qso(self):
        """
        Move to the next QSO in the session.

        Updates current QSO index and loads the next QSO. If all QSOs
        are complete, transitions to 'complete' state.

        Raises:
            RuntimeError: If not in transcribing state
        """
        if self.state != 'transcribing':
            raise RuntimeError("Can only advance to next QSO after transcribing")

        # Mark current QSO as completed
        self.qsos_completed += 1

        # Move to next QSO
        self.current_qso_index += 1

        # Check if session is complete
        if self.current_qso_index >= len(self.qsos):
            self.current_qso = None
            self._update_state('complete')
            self._update_progress()
            return

        # Load next QSO
        self.current_qso = self.qsos[self.current_qso_index]
        self._update_state('ready')
        self._update_progress()

    def skip_current_qso(self):
        """
        Skip the current QSO without transcribing.

        Raises:
            RuntimeError: If not in valid state to skip
        """
        if self.state not in ('ready', 'transcribing', 'playing', 'paused'):
            raise RuntimeError(f"Cannot skip QSO in state: {self.state}")

        # Stop playback if playing
        if self.state in ('playing', 'paused'):
            self._stop_playback.set()

        # Move to next QSO
        self.current_qso_index += 1

        # Check if session is complete
        if self.current_qso_index >= len(self.qsos):
            self.current_qso = None
            self._update_state('complete')
            self._update_progress()
            return

        # Load next QSO
        self.current_qso = self.qsos[self.current_qso_index]
        self._update_state('ready')
        self._update_progress()

    def get_current_qso(self) -> Optional[Dict]:
        """
        Get the current QSO data.

        Returns:
            Current QSO dictionary or None if session complete
        """
        return self.current_qso

    def get_current_morse_text(self) -> Optional[str]:
        """
        Get the Morse text for the current QSO.

        Returns:
            Morse-ready text string or None if no current QSO
        """
        if self.current_qso is None:
            return None

        return self.qso_generator.get_morse_text(self.current_qso)

    def get_current_elements(self) -> Optional[Dict]:
        """
        Get the extractable elements from the current QSO.

        Returns elements dictionary for scoring/validation:
        {
            'callsigns': [call1, call2],
            'names': [name1, name2],
            'qths': [qth1, qth2],
            'rsts': [rst1, rst2],
            'rigs': [rig1, rig2],
            'antennas': [ant1, ant2],
            'powers': [pwr1, pwr2]
        }

        Returns:
            Elements dictionary or None if no current QSO
        """
        if self.current_qso is None:
            return None

        return self.qso_generator.extract_qso_elements(self.current_qso)

    def get_progress(self) -> Dict[str, int]:
        """
        Get session progress information.

        Returns:
            Dictionary with progress metrics:
            {
                'current': current QSO index (0-based),
                'total': total QSOs in session,
                'completed': number of QSOs completed,
                'played': number of QSOs played (including replays)
            }
        """
        return {
            'current': self.current_qso_index,
            'total': self.qso_count,
            'completed': self.qsos_completed,
            'played': self.total_qsos_played
        }

    def get_state(self) -> SessionState:
        """
        Get current session state.

        Returns:
            Current state ('ready', 'playing', 'transcribing', 'complete', 'paused', 'stopped')
        """
        return self.state

    def is_playback_active(self) -> bool:
        """
        Check if audio playback is currently active.

        Returns:
            True if playback thread is running
        """
        return (
            self._playback_thread is not None and
            self._playback_thread.is_alive()
        )

    def wait_for_playback_complete(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for current playback to complete.

        Args:
            timeout: Maximum time to wait in seconds (None = wait forever)

        Returns:
            True if playback completed, False if timeout occurred
        """
        return self._playback_complete.wait(timeout=timeout)

    def reset_session(self):
        """
        Reset the session to initial state.

        Stops any active playback and clears all session data.
        """
        # Stop playback if active
        if self.state in ('playing', 'paused'):
            self._stop_playback.set()

        # Wait for playback thread to finish
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=2.0)

        # Reset state
        self.qsos = []
        self.current_qso = None
        self.current_qso_index = 0
        self.qsos_completed = 0
        self.total_qsos_played = 0
        self._update_state('ready')

    def __repr__(self):
        """String representation of session."""
        return (
            f"QSOPracticeSession("
            f"state={self.state}, "
            f"qso_count={self.qso_count}, "
            f"current={self.current_qso_index}, "
            f"completed={self.qsos_completed})"
        )


# Module version
__version__ = '1.0.0'
