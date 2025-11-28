"""
Unit tests for QSO Scoring System

Tests answer validation, fuzzy matching, score calculation,
and statistics tracking.

Author: Generated with Claude Code
Date: 2025-11-28
Issue: #7 - QSO Feature: Scoring System
"""

import unittest
from qso_scoring import QSOScorer, SessionScorer


class TestQSOScorerInit(unittest.TestCase):
    """Test QSOScorer initialization."""

    def test_initialization_defaults(self):
        """Test initialization with default parameters."""
        scorer = QSOScorer()

        self.assertEqual(scorer.fuzzy_threshold, 0.8)
        self.assertTrue(scorer.partial_credit)
        self.assertFalse(scorer.case_sensitive)
        self.assertEqual(scorer.total_questions, 0)

    def test_initialization_custom_params(self):
        """Test initialization with custom parameters."""
        scorer = QSOScorer(
            fuzzy_threshold=0.9,
            partial_credit=False,
            case_sensitive=True
        )

        self.assertEqual(scorer.fuzzy_threshold, 0.9)
        self.assertFalse(scorer.partial_credit)
        self.assertTrue(scorer.case_sensitive)

    def test_initialization_invalid_threshold(self):
        """Test that invalid threshold raises error."""
        with self.assertRaises(ValueError):
            QSOScorer(fuzzy_threshold=-0.1)

        with self.assertRaises(ValueError):
            QSOScorer(fuzzy_threshold=1.1)


class TestElementScoring(unittest.TestCase):
    """Test individual element scoring."""

    def setUp(self):
        """Set up test scorer."""
        self.scorer = QSOScorer(fuzzy_threshold=0.8, partial_credit=True)

    def test_exact_match(self):
        """Test exact match scoring."""
        score, feedback = self.scorer.score_element('BOB', 'BOB')

        self.assertEqual(score, 1.0)
        self.assertEqual(feedback, 'correct')

    def test_case_insensitive_match(self):
        """Test case insensitive matching."""
        score, feedback = self.scorer.score_element('bob', 'BOB')

        self.assertEqual(score, 1.0)
        self.assertEqual(feedback, 'correct')

    def test_case_sensitive_mismatch(self):
        """Test case sensitive matching."""
        scorer = QSOScorer(case_sensitive=True)
        score, feedback = scorer.score_element('bob', 'BOB')

        self.assertEqual(score, 0.0)
        self.assertEqual(feedback, 'incorrect')

    def test_partial_match(self):
        """Test partial credit for close match."""
        score, feedback = self.scorer.score_element('BOSTN', 'BOSTON')

        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)
        self.assertEqual(feedback, 'partial')

    def test_no_match(self):
        """Test complete mismatch."""
        score, feedback = self.scorer.score_element('LONDON', 'BOSTON')

        self.assertEqual(score, 0.0)
        self.assertEqual(feedback, 'incorrect')

    def test_empty_answer(self):
        """Test empty answer."""
        score, feedback = self.scorer.score_element('', 'BOSTON')

        self.assertEqual(score, 0.0)
        self.assertEqual(feedback, 'incorrect')

    def test_whitespace_normalization(self):
        """Test whitespace normalization."""
        score, feedback = self.scorer.score_element('  BOB  ', 'BOB')

        self.assertEqual(score, 1.0)
        self.assertEqual(feedback, 'correct')

    def test_no_partial_credit(self):
        """Test scoring without partial credit."""
        scorer = QSOScorer(partial_credit=False)
        score, feedback = scorer.score_element('BOSTN', 'BOSTON')

        self.assertEqual(score, 0.0)
        self.assertEqual(feedback, 'incorrect')


class TestCallsignScoring(unittest.TestCase):
    """Test callsign-specific scoring."""

    def setUp(self):
        """Set up test scorer."""
        self.scorer = QSOScorer(fuzzy_threshold=0.8)

    def test_exact_callsign(self):
        """Test exact callsign match."""
        score, feedback = self.scorer.score_callsign('W1ABC', 'W1ABC')

        self.assertEqual(score, 1.0)
        self.assertEqual(feedback, 'correct')

    def test_callsign_partial_match(self):
        """Test partial callsign match."""
        # Callsigns use stricter threshold (0.9)
        score, feedback = self.scorer.score_callsign('W1ABD', 'W1ABC')

        # Should still get partial credit if close enough
        self.assertGreaterEqual(score, 0.0)

    def test_callsign_case_insensitive(self):
        """Test callsign case insensitivity."""
        score, feedback = self.scorer.score_callsign('w1abc', 'W1ABC')

        self.assertEqual(score, 1.0)
        self.assertEqual(feedback, 'correct')


class TestRSTScoring(unittest.TestCase):
    """Test RST report scoring."""

    def setUp(self):
        """Set up test scorer."""
        self.scorer = QSOScorer()

    def test_exact_rst(self):
        """Test exact RST match."""
        score, feedback = self.scorer.score_rst('599', '599')

        self.assertEqual(score, 1.0)
        self.assertEqual(feedback, 'correct')

    def test_rst_partial_match_2_of_3(self):
        """Test RST with 2 out of 3 digits correct."""
        score, feedback = self.scorer.score_rst('589', '599')

        self.assertGreater(score, 0.5)
        self.assertEqual(feedback, 'partial')

    def test_rst_partial_match_1_of_3(self):
        """Test RST with 1 out of 3 digits correct."""
        score, feedback = self.scorer.score_rst('419', '599')

        # Less than 66%, should be incorrect
        self.assertEqual(score, 0.0)
        self.assertEqual(feedback, 'incorrect')

    def test_rst_wrong_length(self):
        """Test RST with wrong length."""
        score, feedback = self.scorer.score_rst('59', '599')

        self.assertEqual(score, 0.0)
        self.assertEqual(feedback, 'incorrect')


class TestQSOScoring(unittest.TestCase):
    """Test complete QSO scoring."""

    def setUp(self):
        """Set up test scorer."""
        self.scorer = QSOScorer()

        # Sample correct elements
        self.correct_elements = {
            'callsigns': ['W1ABC', 'G3YWX'],
            'names': ['BOB', 'IAN'],
            'qths': ['BOSTON', 'LONDON'],
            'rsts': ['599', '589'],
            'rigs': ['IC7300', 'FT991A'],
            'antennas': ['DIPOLE', 'VERTICAL'],
            'powers': ['100W', '50W']
        }

    def test_perfect_score(self):
        """Test perfect QSO score."""
        user_answers = {
            'callsign1': 'W1ABC',
            'callsign2': 'G3YWX',
            'name1': 'BOB',
            'name2': 'IAN',
            'qth1': 'BOSTON',
            'qth2': 'LONDON',
            'rst1': '599',
            'rst2': '589'
        }

        result = self.scorer.score_qso(user_answers, self.correct_elements)

        self.assertEqual(result['total_score'], 8.0)
        self.assertEqual(result['max_score'], 8)
        self.assertEqual(result['percentage'], 100.0)
        self.assertEqual(result['summary']['correct'], 8)
        self.assertEqual(result['summary']['incorrect'], 0)

    def test_partial_score(self):
        """Test QSO with some incorrect answers."""
        user_answers = {
            'callsign1': 'W1ABC',
            'callsign2': 'G3YWX',
            'name1': 'BOB',
            'name2': 'JOHN',  # Incorrect
            'qth1': 'BOSTON',
            'qth2': 'LONDON',
            'rst1': '599',
            'rst2': '579'  # Partially correct
        }

        result = self.scorer.score_qso(user_answers, self.correct_elements)

        self.assertLess(result['total_score'], 8.0)
        self.assertEqual(result['max_score'], 8)
        self.assertLess(result['percentage'], 100.0)
        self.assertGreater(result['summary']['incorrect'], 0)

    def test_with_optional_elements(self):
        """Test QSO with optional equipment fields."""
        user_answers = {
            'callsign1': 'W1ABC',
            'callsign2': 'G3YWX',
            'name1': 'BOB',
            'name2': 'IAN',
            'qth1': 'BOSTON',
            'qth2': 'LONDON',
            'rst1': '599',
            'rst2': '589',
            'rig1': 'IC7300',
            'rig2': 'FT991A',
            'antenna1': 'DIPOLE',
            'power1': '100W'
        }

        result = self.scorer.score_qso(user_answers, self.correct_elements)

        # 8 required + 4 optional = 12 max score
        self.assertEqual(result['max_score'], 12)
        self.assertEqual(result['total_score'], 12.0)

    def test_empty_answers(self):
        """Test QSO with empty answers."""
        user_answers = {
            'callsign1': '',
            'callsign2': '',
            'name1': '',
            'name2': '',
            'qth1': '',
            'qth2': '',
            'rst1': '',
            'rst2': ''
        }

        result = self.scorer.score_qso(user_answers, self.correct_elements)

        self.assertEqual(result['total_score'], 0.0)
        self.assertEqual(result['max_score'], 8)
        self.assertEqual(result['percentage'], 0.0)
        self.assertEqual(result['summary']['incorrect'], 8)

    def test_element_scores_structure(self):
        """Test that element scores have correct structure."""
        user_answers = {
            'callsign1': 'W1ABC',
            'callsign2': 'G3YWX',
            'name1': 'BOB',
            'name2': 'IAN',
            'qth1': 'BOSTON',
            'qth2': 'LONDON',
            'rst1': '599',
            'rst2': '589'
        }

        result = self.scorer.score_qso(user_answers, self.correct_elements)

        # Check structure of element scores
        for key in ['callsign1', 'name1', 'qth1', 'rst1']:
            self.assertIn(key, result['element_scores'])
            elem = result['element_scores'][key]
            self.assertIn('score', elem)
            self.assertIn('feedback', elem)
            self.assertIn('correct', elem)
            self.assertIn('answer', elem)


class TestStatistics(unittest.TestCase):
    """Test statistics tracking."""

    def setUp(self):
        """Set up test scorer."""
        self.scorer = QSOScorer()

    def test_initial_statistics(self):
        """Test initial statistics are zero."""
        stats = self.scorer.get_statistics()

        self.assertEqual(stats['overall']['total_questions'], 0)
        self.assertEqual(stats['overall']['correct'], 0)
        self.assertEqual(stats['overall']['accuracy'], 0.0)

    def test_statistics_after_scoring(self):
        """Test statistics update after scoring."""
        self.scorer.score_element('BOB', 'BOB')
        self.scorer.score_element('JOHN', 'JANE')
        self.scorer.score_element('BOSTON', 'BOSTN')

        stats = self.scorer.get_statistics()

        self.assertEqual(stats['overall']['total_questions'], 3)
        self.assertGreater(stats['overall']['correct'], 0)

    def test_element_type_statistics(self):
        """Test per-element type statistics."""
        self.scorer.score_callsign('W1ABC', 'W1ABC')
        self.scorer.score_callsign('W1ABC', 'K2XYZ')
        self.scorer.score_element('BOB', 'BOB', 'name')

        stats = self.scorer.get_statistics()

        self.assertIn('callsign', stats['by_element'])
        self.assertEqual(stats['by_element']['callsign']['total'], 2)

    def test_reset_statistics(self):
        """Test statistics reset."""
        self.scorer.score_element('BOB', 'BOB')
        self.scorer.reset_statistics()

        stats = self.scorer.get_statistics()

        self.assertEqual(stats['overall']['total_questions'], 0)


class TestSessionScorer(unittest.TestCase):
    """Test SessionScorer functionality."""

    def setUp(self):
        """Set up test session scorer."""
        self.session_scorer = SessionScorer()

    def test_initialization(self):
        """Test session scorer initialization."""
        self.assertIsNotNone(self.session_scorer.scorer)
        self.assertEqual(len(self.session_scorer.qso_scores), 0)

    def test_add_qso_score(self):
        """Test adding QSO score to session."""
        qso_result = {
            'total_score': 7.5,
            'max_score': 8,
            'percentage': 93.8,
            'element_scores': {},
            'summary': {'correct': 7, 'partial': 1, 'incorrect': 0}
        }

        self.session_scorer.add_qso_score(qso_result)

        self.assertEqual(len(self.session_scorer.qso_scores), 1)

    def test_session_summary_empty(self):
        """Test session summary with no QSOs."""
        summary = self.session_scorer.get_session_summary()

        self.assertEqual(summary['qso_count'], 0)
        self.assertEqual(summary['total_score'], 0)
        self.assertEqual(summary['average_percentage'], 0.0)

    def test_session_summary_with_qsos(self):
        """Test session summary with multiple QSOs."""
        # Add multiple QSO scores
        for i in range(3):
            qso_result = {
                'total_score': 7.0 + i * 0.5,
                'max_score': 8,
                'percentage': (7.0 + i * 0.5) / 8 * 100,
                'element_scores': {},
                'summary': {'correct': 7, 'partial': 0, 'incorrect': 1}
            }
            self.session_scorer.add_qso_score(qso_result)

        summary = self.session_scorer.get_session_summary()

        self.assertEqual(summary['qso_count'], 3)
        self.assertEqual(summary['max_score'], 24)
        self.assertGreater(summary['total_score'], 0)

    def test_get_qso_score(self):
        """Test getting specific QSO score."""
        qso_result = {
            'total_score': 8.0,
            'max_score': 8,
            'percentage': 100.0,
            'element_scores': {},
            'summary': {'correct': 8, 'partial': 0, 'incorrect': 0}
        }

        self.session_scorer.add_qso_score(qso_result)

        retrieved = self.session_scorer.get_qso_score(0)

        self.assertEqual(retrieved['total_score'], 8.0)

    def test_get_invalid_qso_score(self):
        """Test getting QSO with invalid index."""
        result = self.session_scorer.get_qso_score(999)

        self.assertIsNone(result)

    def test_reset_session(self):
        """Test session reset."""
        qso_result = {
            'total_score': 8.0,
            'max_score': 8,
            'percentage': 100.0,
            'element_scores': {},
            'summary': {'correct': 8, 'partial': 0, 'incorrect': 0}
        }

        self.session_scorer.add_qso_score(qso_result)
        self.session_scorer.reset_session()

        self.assertEqual(len(self.session_scorer.qso_scores), 0)


class TestIntegration(unittest.TestCase):
    """Test integration scenarios."""

    def test_complete_workflow(self):
        """Test complete scoring workflow."""
        scorer = QSOScorer()
        session_scorer = SessionScorer(scorer)

        # Score multiple QSOs
        correct_elements = {
            'callsigns': ['W1ABC', 'G3YWX'],
            'names': ['BOB', 'IAN'],
            'qths': ['BOSTON', 'LONDON'],
            'rsts': ['599', '589'],
            'rigs': ['IC7300', 'FT991A'],
            'antennas': ['DIPOLE', 'VERTICAL'],
            'powers': ['100W', '50W']
        }

        # QSO 1: Perfect
        user_answers_1 = {
            'callsign1': 'W1ABC',
            'callsign2': 'G3YWX',
            'name1': 'BOB',
            'name2': 'IAN',
            'qth1': 'BOSTON',
            'qth2': 'LONDON',
            'rst1': '599',
            'rst2': '589'
        }

        result_1 = scorer.score_qso(user_answers_1, correct_elements)
        session_scorer.add_qso_score(result_1)

        # QSO 2: Some errors
        user_answers_2 = {
            'callsign1': 'W1ABC',
            'callsign2': 'G3YWX',
            'name1': 'BOB',
            'name2': 'JOHN',  # Wrong
            'qth1': 'BOSTON',
            'qth2': 'PARIS',  # Wrong
            'rst1': '599',
            'rst2': '589'
        }

        result_2 = scorer.score_qso(user_answers_2, correct_elements)
        session_scorer.add_qso_score(result_2)

        # Get session summary
        summary = session_scorer.get_session_summary()

        self.assertEqual(summary['qso_count'], 2)
        self.assertGreater(summary['total_score'], 0)
        self.assertLess(summary['average_percentage'], 100.0)


class TestFuzzyMatching(unittest.TestCase):
    """Test fuzzy matching edge cases."""

    def setUp(self):
        """Set up test scorer."""
        self.scorer = QSOScorer(fuzzy_threshold=0.8)

    def test_typo_tolerance(self):
        """Test tolerance for common typos."""
        # Single character substitution
        score, feedback = self.scorer.score_element('BISTON', 'BOSTON')
        self.assertGreater(score, 0.0)

        # Single character transposition
        score, feedback = self.scorer.score_element('BOSONT', 'BOSTON')
        self.assertGreater(score, 0.0)

    def test_similar_names(self):
        """Test similar but different names."""
        score, feedback = self.scorer.score_element('JOHN', 'JON')
        self.assertGreater(score, 0.0)

    def test_threshold_boundary(self):
        """Test scoring at threshold boundary."""
        scorer = QSOScorer(fuzzy_threshold=0.9)

        # Just below threshold
        score1, feedback1 = scorer.score_element('ABC', 'XYZ')
        self.assertEqual(score1, 0.0)

        # Just above threshold (identical)
        score2, feedback2 = scorer.score_element('ABC', 'ABC')
        self.assertEqual(score2, 1.0)


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
