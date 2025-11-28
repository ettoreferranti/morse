"""
Unit tests for QSOPracticeSession class

Tests practice session management, state transitions, audio integration,
and progress tracking.

Author: Generated with Claude Code
Date: 2025-11-28
Issue: #6 - QSO Feature: Practice Session Manager
"""

import unittest
import time
from unittest.mock import Mock, MagicMock, patch
from qso_practice import QSOPracticeSession, SessionState
import qso_data


class MockMorseCode:
    """Mock MorseCode class for testing."""

    def __init__(self, playback_delay: float = 0.1):
        """
        Initialize mock Morse code.

        Args:
            playback_delay: Simulated playback time in seconds
        """
        self.playback_delay = playback_delay
        self.play_string_calls = []
        self.play_morse_calls = []

    def play_string(self, message: str):
        """Mock play_string method."""
        self.play_string_calls.append(message)
        # Simulate playback time
        time.sleep(self.playback_delay)

    def play_morse(self, message: str):
        """Mock play_morse method."""
        self.play_morse_calls.append(message)
        time.sleep(self.playback_delay)


class TestQSOPracticeSessionInit(unittest.TestCase):
    """Test QSOPracticeSession initialization."""

    def test_initialization_defaults(self):
        """Test initialization with default parameters."""
        morse_code = MockMorseCode()
        session = QSOPracticeSession(morse_code=morse_code)

        self.assertEqual(session.qso_count, 5)
        self.assertEqual(session.verbosity, 'medium')
        self.assertIsNone(session.call_region1)
        self.assertIsNone(session.call_region2)
        self.assertIsNone(session.seed)
        self.assertEqual(session.state, 'ready')
        self.assertEqual(session.current_qso_index, 0)
        self.assertEqual(session.qsos_completed, 0)

    def test_initialization_custom_params(self):
        """Test initialization with custom parameters."""
        morse_code = MockMorseCode()
        session = QSOPracticeSession(
            morse_code=morse_code,
            qso_count=10,
            verbosity='chatty',
            call_region1='us',
            call_region2='uk',
            seed=42
        )

        self.assertEqual(session.qso_count, 10)
        self.assertEqual(session.verbosity, 'chatty')
        self.assertEqual(session.call_region1, 'us')
        self.assertEqual(session.call_region2, 'uk')
        self.assertEqual(session.seed, 42)

    def test_initialization_invalid_qso_count(self):
        """Test that invalid qso_count raises error."""
        morse_code = MockMorseCode()

        with self.assertRaises(ValueError):
            QSOPracticeSession(morse_code=morse_code, qso_count=0)

        with self.assertRaises(ValueError):
            QSOPracticeSession(morse_code=morse_code, qso_count=101)

        with self.assertRaises(ValueError):
            QSOPracticeSession(morse_code=morse_code, qso_count='invalid')

    def test_initialization_invalid_verbosity(self):
        """Test that invalid verbosity raises error."""
        morse_code = MockMorseCode()

        with self.assertRaises(ValueError):
            QSOPracticeSession(morse_code=morse_code, verbosity='invalid')


class TestSessionStateManagement(unittest.TestCase):
    """Test session state transitions."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode(playback_delay=0.05)
        self.session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=3,
            verbosity='minimal'
        )

    def test_initial_state(self):
        """Test that session starts in 'ready' state."""
        self.assertEqual(self.session.get_state(), 'ready')

    def test_start_session_state_transition(self):
        """Test state transition when starting session."""
        self.session.start_session()

        self.assertEqual(self.session.get_state(), 'ready')
        self.assertEqual(len(self.session.qsos), 3)
        self.assertIsNotNone(self.session.current_qso)

    def test_play_qso_state_transition(self):
        """Test state transition when playing QSO."""
        self.session.start_session()
        self.session.play_current_qso()

        # Should transition to 'playing'
        self.assertEqual(self.session.get_state(), 'playing')

        # Wait for playback to complete
        self.session.wait_for_playback_complete(timeout=1.0)

        # Should transition to 'transcribing'
        self.assertEqual(self.session.get_state(), 'transcribing')

    def test_next_qso_state_transition(self):
        """Test state transition when moving to next QSO."""
        self.session.start_session()
        self.session.play_current_qso()
        self.session.wait_for_playback_complete(timeout=1.0)

        self.session.next_qso()

        # Should return to 'ready' for next QSO
        self.assertEqual(self.session.get_state(), 'ready')
        self.assertEqual(self.session.current_qso_index, 1)

    def test_complete_state_transition(self):
        """Test state transition when session completes."""
        self.session.start_session()

        # Complete all QSOs
        for _ in range(3):
            self.session.play_current_qso()
            self.session.wait_for_playback_complete(timeout=1.0)
            self.session.next_qso()

        # Should transition to 'complete'
        self.assertEqual(self.session.get_state(), 'complete')
        self.assertIsNone(self.session.current_qso)


class TestQSOPlayback(unittest.TestCase):
    """Test QSO audio playback functionality."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode(playback_delay=0.05)
        self.session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=2,
            verbosity='minimal'
        )
        self.session.start_session()

    def test_play_current_qso(self):
        """Test playing current QSO."""
        self.session.play_current_qso()

        # Should be in playing state
        self.assertEqual(self.session.get_state(), 'playing')

        # Wait for completion
        completed = self.session.wait_for_playback_complete(timeout=1.0)
        self.assertTrue(completed)

        # Should have called play_string
        self.assertEqual(len(self.morse_code.play_string_calls), 1)

    def test_replay_current_qso(self):
        """Test replaying current QSO."""
        self.session.play_current_qso()
        self.session.wait_for_playback_complete(timeout=1.0)

        # Replay
        self.session.replay_current_qso()
        self.session.wait_for_playback_complete(timeout=1.0)

        # Should have called play_string twice
        self.assertEqual(len(self.morse_code.play_string_calls), 2)

    def test_replay_invalid_state(self):
        """Test that replay fails in invalid state."""
        # Cannot replay before playing
        with self.assertRaises(RuntimeError):
            self.session.replay_current_qso()

    def test_playback_thread_active(self):
        """Test playback thread tracking."""
        self.session.play_current_qso()

        # Thread should be active during playback
        self.assertTrue(self.session.is_playback_active())

        # Wait for completion
        self.session.wait_for_playback_complete(timeout=1.0)

        # Thread should finish
        time.sleep(0.1)  # Allow thread cleanup
        self.assertFalse(self.session.is_playback_active())


class TestPlaybackControl(unittest.TestCase):
    """Test playback control (pause, resume, stop)."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode(playback_delay=0.5)
        self.session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=2
        )
        self.session.start_session()

    def test_stop_playback(self):
        """Test stopping playback."""
        self.session.play_current_qso()

        # Stop playback
        time.sleep(0.1)  # Let playback start
        self.session.stop_playback()

        self.assertEqual(self.session.get_state(), 'stopped')

    def test_pause_playback(self):
        """Test pausing playback."""
        self.session.play_current_qso()

        time.sleep(0.1)  # Let playback start
        self.session.pause_playback()

        self.assertEqual(self.session.get_state(), 'paused')

    def test_resume_playback(self):
        """Test resuming playback."""
        self.session.play_current_qso()

        time.sleep(0.1)
        self.session.pause_playback()
        self.assertEqual(self.session.get_state(), 'paused')

        self.session.resume_playback()
        self.assertEqual(self.session.get_state(), 'playing')

    def test_pause_invalid_state(self):
        """Test that pause fails in invalid state."""
        with self.assertRaises(RuntimeError):
            self.session.pause_playback()

    def test_resume_invalid_state(self):
        """Test that resume fails in invalid state."""
        with self.assertRaises(RuntimeError):
            self.session.resume_playback()

    def test_stop_invalid_state(self):
        """Test that stop fails in invalid state."""
        with self.assertRaises(RuntimeError):
            self.session.stop_playback()


class TestSessionNavigation(unittest.TestCase):
    """Test session navigation (next, skip)."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode(playback_delay=0.05)
        self.session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=3
        )
        self.session.start_session()

    def test_next_qso(self):
        """Test moving to next QSO."""
        self.session.play_current_qso()
        self.session.wait_for_playback_complete(timeout=1.0)

        initial_index = self.session.current_qso_index
        self.session.next_qso()

        self.assertEqual(self.session.current_qso_index, initial_index + 1)
        self.assertEqual(self.session.qsos_completed, 1)

    def test_next_qso_invalid_state(self):
        """Test that next_qso fails in invalid state."""
        with self.assertRaises(RuntimeError):
            self.session.next_qso()

    def test_skip_current_qso(self):
        """Test skipping current QSO."""
        initial_index = self.session.current_qso_index
        self.session.skip_current_qso()

        self.assertEqual(self.session.current_qso_index, initial_index + 1)

    def test_skip_during_playback(self):
        """Test skipping while playback is active."""
        self.session.play_current_qso()

        time.sleep(0.1)  # Let playback start
        self.session.skip_current_qso()

        self.assertEqual(self.session.current_qso_index, 1)

    def test_skip_to_completion(self):
        """Test skipping all QSOs leads to completion."""
        for _ in range(3):
            self.session.skip_current_qso()

        self.assertEqual(self.session.get_state(), 'complete')
        self.assertIsNone(self.session.current_qso)


class TestProgressTracking(unittest.TestCase):
    """Test session progress tracking."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode(playback_delay=0.05)
        self.session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=5
        )
        self.session.start_session()

    def test_initial_progress(self):
        """Test initial progress values."""
        progress = self.session.get_progress()

        self.assertEqual(progress['current'], 0)
        self.assertEqual(progress['total'], 5)
        self.assertEqual(progress['completed'], 0)
        self.assertEqual(progress['played'], 0)

    def test_progress_after_play(self):
        """Test progress after playing QSO."""
        self.session.play_current_qso()
        self.session.wait_for_playback_complete(timeout=1.0)

        progress = self.session.get_progress()

        self.assertEqual(progress['played'], 1)

    def test_progress_after_next(self):
        """Test progress after moving to next QSO."""
        self.session.play_current_qso()
        self.session.wait_for_playback_complete(timeout=1.0)
        self.session.next_qso()

        progress = self.session.get_progress()

        self.assertEqual(progress['current'], 1)
        self.assertEqual(progress['completed'], 1)
        self.assertEqual(progress['played'], 1)

    def test_progress_with_replay(self):
        """Test that replays increment played count."""
        self.session.play_current_qso()
        self.session.wait_for_playback_complete(timeout=1.0)

        self.session.replay_current_qso()
        self.session.wait_for_playback_complete(timeout=1.0)

        progress = self.session.get_progress()

        self.assertEqual(progress['played'], 2)
        self.assertEqual(progress['completed'], 0)


class TestQSODataAccess(unittest.TestCase):
    """Test access to QSO data."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode()
        self.session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=2,
            seed=42
        )
        self.session.start_session()

    def test_get_current_qso(self):
        """Test getting current QSO data."""
        qso = self.session.get_current_qso()

        self.assertIsNotNone(qso)
        self.assertIn('calling_station', qso)
        self.assertIn('responding_station', qso)
        self.assertIn('full_text', qso)

    def test_get_current_morse_text(self):
        """Test getting current Morse text."""
        morse_text = self.session.get_current_morse_text()

        self.assertIsNotNone(morse_text)
        self.assertIsInstance(morse_text, str)
        self.assertIn('CQ', morse_text)

    def test_get_current_elements(self):
        """Test getting current QSO elements."""
        elements = self.session.get_current_elements()

        self.assertIsNotNone(elements)
        self.assertIn('callsigns', elements)
        self.assertIn('names', elements)
        self.assertEqual(len(elements['callsigns']), 2)

    def test_get_data_when_complete(self):
        """Test getting data when session is complete."""
        # Complete all QSOs
        for _ in range(2):
            self.session.skip_current_qso()

        self.assertIsNone(self.session.get_current_qso())
        self.assertIsNone(self.session.get_current_morse_text())
        self.assertIsNone(self.session.get_current_elements())


class TestCallbacks(unittest.TestCase):
    """Test event callbacks."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode(playback_delay=0.05)
        self.session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=2
        )

    def test_state_change_callback(self):
        """Test state change callback."""
        states = []

        def on_state_change(state):
            states.append(state)

        self.session.set_state_change_callback(on_state_change)
        self.session.start_session()

        self.assertIn('ready', states)

    def test_progress_update_callback(self):
        """Test progress update callback."""
        progress_updates = []

        def on_progress(current, total):
            progress_updates.append((current, total))

        self.session.set_progress_update_callback(on_progress)
        self.session.start_session()

        self.assertGreater(len(progress_updates), 0)

    def test_playback_complete_callback(self):
        """Test playback complete callback."""
        callback_called = []

        def on_complete():
            callback_called.append(True)

        self.session.set_playback_complete_callback(on_complete)
        self.session.start_session()
        self.session.play_current_qso()
        self.session.wait_for_playback_complete(timeout=1.0)

        time.sleep(0.1)  # Allow callback to execute
        self.assertEqual(len(callback_called), 1)


class TestSessionReset(unittest.TestCase):
    """Test session reset functionality."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode(playback_delay=0.05)
        self.session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=3
        )

    def test_reset_session(self):
        """Test resetting session."""
        self.session.start_session()
        self.session.play_current_qso()

        self.session.reset_session()

        self.assertEqual(self.session.get_state(), 'ready')
        self.assertEqual(len(self.session.qsos), 0)
        self.assertIsNone(self.session.current_qso)
        self.assertEqual(self.session.current_qso_index, 0)
        self.assertEqual(self.session.qsos_completed, 0)

    def test_reset_stops_playback(self):
        """Test that reset stops active playback."""
        self.session.start_session()
        self.session.play_current_qso()

        time.sleep(0.1)  # Let playback start
        self.session.reset_session()

        # Thread should stop
        time.sleep(0.2)
        self.assertFalse(self.session.is_playback_active())


class TestSessionRestart(unittest.TestCase):
    """Test restarting sessions."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode(playback_delay=0.05)
        self.session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=2
        )

    def test_restart_after_complete(self):
        """Test restarting session after completion."""
        self.session.start_session()

        # Complete session
        for _ in range(2):
            self.session.skip_current_qso()

        self.assertEqual(self.session.get_state(), 'complete')

        # Restart
        self.session.start_session()

        self.assertEqual(self.session.get_state(), 'ready')
        self.assertEqual(self.session.current_qso_index, 0)

    def test_cannot_start_during_playback(self):
        """Test that cannot start during active session."""
        self.session.start_session()
        self.session.play_current_qso()

        with self.assertRaises(RuntimeError):
            self.session.start_session()


class TestIntegration(unittest.TestCase):
    """Test integration with QSOGenerator."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode(playback_delay=0.05)

    def test_integration_with_qso_generator(self):
        """Test that session properly integrates with QSOGenerator."""
        session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=3,
            verbosity='medium',
            call_region1='us',
            call_region2='uk',
            seed=42
        )

        session.start_session()

        # Should generate valid QSOs
        qso = session.get_current_qso()
        self.assertIsNotNone(qso)

        # US call sign should start with W, K, N, or A
        calling_call = qso['calling_station']['callsign']
        self.assertTrue(calling_call[0] in 'WKNA')

        # UK call sign should start with G or M
        responding_call = qso['responding_station']['callsign']
        self.assertTrue(responding_call[0] in 'GM')

    def test_verbosity_propagation(self):
        """Test that verbosity is properly propagated."""
        session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=2,
            verbosity='chatty'
        )

        session.start_session()
        qso = session.get_current_qso()

        self.assertEqual(qso['verbosity'], 'chatty')


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def setUp(self):
        """Set up test session."""
        self.morse_code = MockMorseCode()

    def test_single_qso_session(self):
        """Test session with single QSO."""
        session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=1
        )

        session.start_session()
        session.skip_current_qso()

        self.assertEqual(session.get_state(), 'complete')

    def test_maximum_qso_count(self):
        """Test session with maximum QSO count."""
        session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=100
        )

        session.start_session()

        self.assertEqual(len(session.qsos), 100)

    def test_repr(self):
        """Test string representation."""
        session = QSOPracticeSession(
            morse_code=self.morse_code,
            qso_count=5
        )

        repr_str = repr(session)

        self.assertIn('QSOPracticeSession', repr_str)
        self.assertIn('state=ready', repr_str)
        self.assertIn('qso_count=5', repr_str)


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    result = run_tests()
    exit(0 if result.wasSuccessful() else 1)
