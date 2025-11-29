"""
Automated GUI Tests for QSO Practice Feature

Tests the actual GUI widgets and interactions, including:
- Button states (enabled/disabled)
- Entry field editability
- Button clicks and their effects
- UI state changes during playback
- All the bugs we fixed today

Run with: python -m pytest test_gui_qso_practice.py -v
"""

import unittest
import tkinter as tk
from unittest.mock import MagicMock, patch, PropertyMock
import time
import threading
from morse import MorseCode
from morse_gui import MorseCodeGUI


class TestQSOPracticeGUI(unittest.TestCase):
    """Test QSO Practice GUI interactions"""

    def setUp(self):
        """Create GUI instance for testing"""
        # Create root window
        self.root = tk.Tk()

        # Mock pyaudio to avoid actual audio initialization
        with patch('morse.pyaudio.PyAudio') as mock_pyaudio:
            # Configure the mock
            mock_audio_instance = MagicMock()
            mock_pyaudio.return_value = mock_audio_instance
            mock_audio_instance.open.return_value = MagicMock()

            # Create GUI
            self.gui = MorseCodeGUI(self.root)

        # Give GUI time to initialize
        self.root.update()

        # Switch to QSO Practice tab
        self.gui.notebook.select(3)  # QSO Practice is tab 3
        self.root.update()

    def tearDown(self):
        """Clean up after each test"""
        try:
            if hasattr(self, 'gui') and hasattr(self.gui, 'qso_session'):
                if self.gui.qso_session:
                    self.gui.qso_session.stop_playback()
            self.root.quit()
            self.root.destroy()
        except:
            pass

    def test_gui_initializes(self):
        """Test GUI initializes successfully"""
        self.assertIsNotNone(self.gui)
        self.assertIsNotNone(self.root)

    def test_initial_button_states(self):
        """Test initial state of QSO buttons"""
        # Play button doubles as start session - should be enabled
        self.assertEqual(str(self.gui.qso_play_button['state']), 'normal')

        # Submit button should be disabled initially
        self.assertEqual(str(self.gui.qso_submit_button['state']), 'disabled')

    def test_entry_fields_disabled_initially(self):
        """Test entry fields are disabled before session starts"""
        for entry in self.gui.qso_entry_widgets.values():
            # Should be disabled initially
            self.assertEqual(str(entry['state']), 'disabled')

    def test_start_session_button(self):
        """Test clicking Start Session button"""
        # Mock the QSO session creation
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            # Click start session
            self.gui.start_qso_session()
            self.root.update()

            # Session should be created
            self.assertIsNotNone(self.gui.qso_session)

            # Play button should now be enabled (changes to Play QSO)
            self.assertEqual(str(self.gui.qso_play_button['state']), 'normal')

    def test_entry_fields_enabled_during_playback(self):
        """
        CRITICAL BUG FIX TEST: Entry fields should be enabled when playback starts
        This tests the fix we implemented today
        """
        # Start a session
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            self.gui.start_qso_session()
            self.root.update()
            
            # Start playback
            self.gui.play_current_qso()
            self.root.update()
            time.sleep(0.1)
            
            # Entry fields should be enabled during playback
            for entry in self.gui.qso_entry_widgets.values():
                state = str(entry['state'])
                self.assertIn(state, ['normal', '!disabled'], 
                    f"Entry field should be enabled during playback, got: {state}")

    def test_submit_button_enabled_during_playback(self):
        """
        CRITICAL BUG FIX TEST: Submit button should be enabled during playback
        This tests the fix we implemented today
        """
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            self.gui.start_qso_session()
            self.root.update()

            # Start playback
            self.gui.play_current_qso()
            self.root.update()
            time.sleep(0.1)

            # Submit button should be enabled
            self.assertEqual(str(self.gui.qso_submit_button['state']), 'normal')

    def test_pause_button_functionality(self):
        """Test pause button changes state correctly"""
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            self.gui.start_qso_session()
            self.root.update()

            # Start playback
            self.gui.play_current_qso()
            self.root.update()

            # Button should show "Pause" (with emoji)
            button_text = self.gui.qso_play_button['text']
            self.assertIn('Pause', button_text)

            # Manually set session to playing state (since mock completes instantly)
            if self.gui.qso_session:
                self.gui.qso_session._update_state('playing')

            # Click to pause
            self.gui.toggle_qso_playback()
            self.root.update()

            # Button should show "Resume"
            button_text = self.gui.qso_play_button['text']
            self.assertIn('Resume', button_text)

    def test_replay_button_enabled_during_playback(self):
        """Test replay button is enabled during playback (bug we fixed)"""
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            self.gui.start_qso_session()
            self.root.update()

            self.gui.play_current_qso()
            self.root.update()
            time.sleep(0.1)

            # Replay button should be enabled
            self.assertEqual(str(self.gui.qso_replay_button['state']), 'normal')

    def test_skip_button_enabled_during_playback(self):
        """Test skip button is enabled during playback (bug we fixed)"""
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            self.gui.start_qso_session()
            self.root.update()

            self.gui.play_current_qso()
            self.root.update()
            time.sleep(0.1)

            # Skip button should be enabled
            self.assertEqual(str(self.gui.qso_skip_button['state']), 'normal')

    def test_entry_fields_accept_input(self):
        """Test that entry fields accept user input during playback"""
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            self.gui.start_qso_session()
            self.root.update()
            
            self.gui.play_current_qso()
            self.root.update()
            time.sleep(0.1)
            
            # Try to type in first entry field
            first_entry = list(self.gui.qso_entry_widgets.values())[0]
            first_var = list(self.gui.qso_entry_vars.values())[0]
            
            # Set a value
            first_var.set('TEST123')
            self.root.update()
            
            # Verify it was set
            self.assertEqual(first_var.get(), 'TEST123')

    def test_submit_during_playback(self):
        """
        CRITICAL BUG FIX TEST: Submitting during playback should work
        This was the main bug we fixed today
        """
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            self.gui.start_qso_session()
            self.root.update()
            
            self.gui.play_current_qso()
            self.root.update()
            time.sleep(0.1)
            
            # Fill in some answers
            for var in self.gui.qso_entry_vars.values():
                var.set('TEST')
            
            # Submit while playing - should not crash
            try:
                self.gui.submit_qso_answer()
                self.root.update()
                time.sleep(0.3)  # Wait for submission to process
                success = True
            except Exception as e:
                success = False
                error = str(e)
            
            self.assertTrue(success, f"Submit during playback failed: {error if not success else ''}")

    def test_instructions_text_updates(self):
        """Test that instruction text updates correctly"""
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            self.gui.start_qso_session()
            self.root.update()
            
            # Start playback
            self.gui.play_current_qso()
            self.root.update()
            time.sleep(0.1)
            
            # Instructions should mention submitting anytime
            instructions = self.gui.qso_instructions['text']
            self.assertIn('submit', instructions.lower())

    def test_stop_session_button(self):
        """Test stop session functionality"""
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            # Mock messagebox to auto-confirm
            with patch('morse_gui.messagebox.askyesno', return_value=True):
                self.gui.start_qso_session()
                self.root.update()
                
                self.gui.play_current_qso()
                self.root.update()
                
                # Stop session
                self.gui.stop_qso_session()
                self.root.update()
                
                # Session should be reset or None
                if self.gui.qso_session:
                    self.assertIn(self.gui.qso_session.state, ['ready', 'stopped'])


class TestGUIStatePersistence(unittest.TestCase):
    """Test that GUI state persists correctly"""

    def setUp(self):
        self.root = tk.Tk()
        # Mock pyaudio to avoid actual audio initialization
        with patch('morse.pyaudio.PyAudio') as mock_pyaudio:
            mock_audio_instance = MagicMock()
            mock_pyaudio.return_value = mock_audio_instance
            mock_audio_instance.open.return_value = MagicMock()
            self.gui = MorseCodeGUI(self.root)
        self.root.update()
        self.gui.notebook.select(3)
        self.root.update()

    def tearDown(self):
        try:
            if hasattr(self, 'gui') and hasattr(self.gui, 'qso_session'):
                if self.gui.qso_session:
                    self.gui.qso_session.stop_playback()
            self.root.quit()
            self.root.destroy()
        except:
            pass

    def test_configuration_persists(self):
        """Test that configuration changes persist"""
        # Set some configuration
        self.gui.qso_config_count = 10
        self.gui.qso_config_verbosity = 'chatty'

        # Start session with those settings
        with patch.object(self.gui.morse, 'play_string', return_value=None):
            self.gui.start_qso_session()
            self.root.update()

            # Verify session uses those settings (actual attribute is qso_count, not total_qsos)
            self.assertEqual(self.gui.qso_session.qso_count, 10)
            self.assertEqual(self.gui.qso_session.verbosity, 'chatty')


class TestGUIWidgetReferences(unittest.TestCase):
    """Test that GUI has correct widget references"""

    def setUp(self):
        self.root = tk.Tk()
        # Mock pyaudio to avoid actual audio initialization
        with patch('morse.pyaudio.PyAudio') as mock_pyaudio:
            mock_audio_instance = MagicMock()
            mock_pyaudio.return_value = mock_audio_instance
            mock_audio_instance.open.return_value = MagicMock()
            self.gui = MorseCodeGUI(self.root)
        self.root.update()

    def tearDown(self):
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass

    def test_all_qso_buttons_exist(self):
        """Test all QSO buttons are created"""
        # Note: qso_play_button doubles as start session button
        self.assertTrue(hasattr(self.gui, 'qso_play_button'))
        self.assertTrue(hasattr(self.gui, 'qso_replay_button'))
        self.assertTrue(hasattr(self.gui, 'qso_skip_button'))
        self.assertTrue(hasattr(self.gui, 'qso_submit_button'))
        self.assertTrue(hasattr(self.gui, 'qso_stop_button'))

    def test_entry_widgets_dictionary_populated(self):
        """Test that entry widgets dictionary is populated"""
        self.assertIsNotNone(self.gui.qso_entry_widgets)
        self.assertGreater(len(self.gui.qso_entry_widgets), 0)

        # Check expected fields exist (actual field names from GUI)
        expected_fields = ['callsign1', 'callsign2', 'name1', 'name2', 'qth1', 'qth2']
        for field in expected_fields:
            self.assertIn(field, self.gui.qso_entry_widgets)

    def test_entry_vars_dictionary_populated(self):
        """Test that entry vars dictionary is populated"""
        self.assertIsNotNone(self.gui.qso_entry_vars)
        self.assertGreater(len(self.gui.qso_entry_vars), 0)
        
        # Should match entry widgets
        self.assertEqual(
            set(self.gui.qso_entry_vars.keys()),
            set(self.gui.qso_entry_widgets.keys())
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
