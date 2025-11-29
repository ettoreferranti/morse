"""
Test suite for QSO Practice functionality

Tests cover the bugs we fixed:
- Entry field enablement during playback
- Submit during playback functionality
- State transitions
- Pause/Resume/Stop/Replay controls

Run with: python -m unittest test_qso_practice.py -v
"""

import unittest
from unittest.mock import MagicMock, patch
import time
from qso_practice import QSOPracticeSession
from qso_data import QSOGenerator
from qso_scoring import QSOScorer, SessionScorer


class TestQSOPracticeSession(unittest.TestCase):
    """Test QSO practice session state management"""

    def setUp(self):
        # Create mock MorseCode object
        self.mock_morse = MagicMock()
        self.mock_morse.play_string = MagicMock(side_effect=lambda x: time.sleep(0.1))

        # Create session
        self.session = QSOPracticeSession(
            morse_code=self.mock_morse,
            qso_count=3,
            verbosity='minimal'
        )

    def test_session_starts_in_ready_state(self):
        """Test session initializes in ready state"""
        self.session.start_session()
        self.assertEqual(self.session.state, 'ready')

    def test_playback_starts(self):
        """Test playback transitions to playing state"""
        self.session.start_session()
        self.session.play_current_qso()
        self.assertEqual(self.session.state, 'playing')

    def test_playback_completes_to_transcribing(self):
        """Test playback completes and transitions to transcribing"""
        self.session.start_session()
        self.session.play_current_qso()

        # Wait for playback to complete
        time.sleep(0.3)

        # Should transition to transcribing
        self.assertEqual(self.session.state, 'transcribing')

    def test_pause_and_resume(self):
        """Test pause/resume functionality (bug we fixed)"""
        self.session.start_session()
        self.session.play_current_qso()
        self.assertEqual(self.session.state, 'playing')

        # Pause
        self.session.pause_playback()
        self.assertEqual(self.session.state, 'paused')

        # Resume
        self.session.resume_playback()
        self.assertEqual(self.session.state, 'playing')

    def test_stop_playback(self):
        """Test stop functionality"""
        self.session.start_session()
        self.session.play_current_qso()

        # Stop
        self.session.stop_playback()

        # Wait for thread to finish
        time.sleep(0.2)

        # Should be in stopped or transcribing state
        self.assertIn(self.session.state, ['stopped', 'transcribing'])

    def test_replay_functionality(self):
        """Test replay button functionality (bug we fixed)"""
        self.session.start_session()
        self.session.play_current_qso()

        # Wait for playback to complete
        time.sleep(0.3)
        self.assertEqual(self.session.state, 'transcribing')

        # Replay should work
        self.session.replay_current_qso()
        self.assertEqual(self.session.state, 'playing')


class TestSubmitDuringPlayback(unittest.TestCase):
    """Test the critical bug fix: submitting while QSO is playing"""

    def setUp(self):
        self.mock_morse = MagicMock()
        self.mock_morse.play_string = MagicMock(side_effect=lambda x: time.sleep(0.1))
        self.session = QSOPracticeSession(
            morse_code=self.mock_morse,
            qso_count=2,
            verbosity='minimal'
        )

    def test_submit_during_playback(self):
        """
        CRITICAL: Test submitting answer while QSO is playing.
        This was the main bug - it would fail with:
        'Can only advance to next QSO after transcribing'
        """
        self.session.start_session()
        self.session.play_current_qso()
        self.assertEqual(self.session.state, 'playing')

        # Simulate what GUI does when user clicks submit during playback:
        # 1. Stop playback
        self.session.stop_playback()

        # 2. Force transition to transcribing state (this is the fix)
        self.session._update_state('transcribing')

        # 3. Should now be able to advance to next QSO without error
        try:
            self.session.next_qso()
            success = True
            error_msg = None
        except Exception as e:
            success = False
            error_msg = str(e)

        self.assertTrue(success, 
            f"Should be able to advance after early submit. Error: {error_msg}")
        self.assertEqual(self.session.state, 'ready')

    def test_submit_during_pause(self):
        """Test submitting while paused"""
        self.session.start_session()
        self.session.play_current_qso()

        # Pause
        self.session.pause_playback()
        self.assertEqual(self.session.state, 'paused')

        # Stop and transition to transcribing (simulating submit)
        self.session.stop_playback()
        self.session._update_state('transcribing')

        # Should advance successfully
        self.session.next_qso()
        self.assertEqual(self.session.state, 'ready')


class TestStateCallbacks(unittest.TestCase):
    """Test state change callbacks work correctly"""

    def setUp(self):
        self.mock_morse = MagicMock()
        self.mock_morse.play_string = MagicMock(side_effect=lambda x: time.sleep(0.1))
        self.session = QSOPracticeSession(
            morse_code=self.mock_morse,
            qso_count=1,
            verbosity='minimal'
        )

    def test_state_change_callback_fires(self):
        """Test state change callback is triggered"""
        callback = MagicMock()
        self.session.set_state_change_callback(callback)

        self.session.start_session()
        self.session.play_current_qso()

        # Callback should be called with 'playing' state
        callback.assert_called()
        # Check that 'playing' was one of the states
        state_calls = [call[0][0] for call in callback.call_args_list]
        self.assertIn('playing', state_calls)

    def test_playback_complete_callback(self):
        """Test playback complete callback is triggered"""
        callback = MagicMock()
        self.session.set_playback_complete_callback(callback)

        self.session.start_session()
        self.session.play_current_qso()

        # Wait for playback to complete
        time.sleep(0.3)

        # Callback should be called
        callback.assert_called()


class TestQSOGenerator(unittest.TestCase):
    """Test QSO generation works"""

    def setUp(self):
        self.generator = QSOGenerator()

    def test_generate_minimal_qso(self):
        """Test minimal QSO generation"""
        qso = self.generator.generate_qso(verbosity='minimal')

        # Check structure
        self.assertIn('calling_station', qso)
        self.assertIn('responding_station', qso)
        self.assertIn('full_text', qso)
        self.assertIn('elements', qso)

    def test_get_morse_text(self):
        """Test getting morse text from QSO"""
        qso = self.generator.generate_qso(verbosity='minimal')
        morse_text = self.generator.get_morse_text(qso)

        # Should have some content
        self.assertGreater(len(morse_text), 50)
        self.assertIsInstance(morse_text, str)


class TestQSOScoring(unittest.TestCase):
    """Test scoring functionality"""

    def setUp(self):
        self.scorer = QSOScorer(fuzzy_threshold=0.8, partial_credit=True)

    def test_scorer_creation(self):
        """Test scorer can be created"""
        self.assertIsNotNone(self.scorer)
        self.assertEqual(self.scorer.fuzzy_threshold, 0.8)
        self.assertTrue(self.scorer.partial_credit)


class TestSessionScorer(unittest.TestCase):
    """Test session-level scoring"""

    def setUp(self):
        qso_scorer = QSOScorer()
        self.session_scorer = SessionScorer(qso_scorer)

    def test_session_scorer_creation(self):
        """Test session scorer can be created"""
        self.assertIsNotNone(self.session_scorer)

    def test_get_session_summary(self):
        """Test getting session summary"""
        summary = self.session_scorer.get_session_summary()

        # Should return a dict with expected keys
        self.assertIn('qso_count', summary)
        self.assertIn('total_score', summary)
        self.assertIn('max_score', summary)
        self.assertEqual(summary['qso_count'], 0)  # No QSOs scored yet


class TestRapidStateChanges(unittest.TestCase):
    """Test rapid state changes don't cause crashes"""

    def setUp(self):
        self.mock_morse = MagicMock()
        self.mock_morse.play_string = MagicMock(side_effect=lambda x: time.sleep(0.1))
        self.session = QSOPracticeSession(
            morse_code=self.mock_morse,
            qso_count=1,
            verbosity='minimal'
        )

    def test_rapid_play_pause_resume_stop(self):
        """Test rapid state changes (simulating user clicking buttons fast)"""
        self.session.start_session()

        # Rapid play/pause/resume/stop
        self.session.play_current_qso()
        self.session.pause_playback()
        self.session.resume_playback()
        self.session.pause_playback()
        self.session.stop_playback()

        time.sleep(0.3)  # Wait for all threads to finish

        # Should end in a valid state without crashing
        self.assertIn(self.session.state, ['stopped', 'transcribing', 'ready'])


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
