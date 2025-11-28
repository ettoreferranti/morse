"""
QSO Scoring and Validation System

Implements answer validation, fuzzy matching for partial credit,
score calculation, and session statistics tracking.

Author: Generated with Claude Code
Date: 2025-11-28
Issue: #7 - QSO Feature: Scoring System
Version: 1.0.0
"""

from typing import Dict, List, Optional, Tuple
import re
from difflib import SequenceMatcher


class QSOScorer:
    """
    Scores user answers against QSO elements with fuzzy matching.

    Provides partial credit for close answers and tracks statistics
    across practice sessions.

    Scoring Rules:
    - Exact match: 100% credit
    - Close match (similarity >= threshold): Partial credit
    - No match: 0% credit

    Elements scored:
    - Callsigns (2 per QSO)
    - Names (2 per QSO)
    - QTHs/Locations (2 per QSO)
    - RST reports (2 per QSO)
    - Equipment (rigs, antennas, power) - optional

    Example usage:
        scorer = QSOScorer(fuzzy_threshold=0.8)

        # Score a single element
        score = scorer.score_callsign('W1ABC', 'W1ABC')  # 1.0

        # Score a complete QSO
        user_answers = {
            'callsign1': 'W1ABC',
            'callsign2': 'G3YWX',
            'name1': 'BOB',
            'name2': 'IAN',
            # ...
        }
        result = scorer.score_qso(user_answers, correct_elements)
    """

    def __init__(
        self,
        fuzzy_threshold: float = 0.8,
        partial_credit: bool = True,
        case_sensitive: bool = False
    ):
        """
        Initialize QSO scorer.

        Args:
            fuzzy_threshold: Minimum similarity for partial credit (0.0-1.0)
            partial_credit: Whether to award partial credit for close matches
            case_sensitive: Whether comparisons are case-sensitive
        """
        if not 0.0 <= fuzzy_threshold <= 1.0:
            raise ValueError("fuzzy_threshold must be between 0.0 and 1.0")

        self.fuzzy_threshold = fuzzy_threshold
        self.partial_credit = partial_credit
        self.case_sensitive = case_sensitive

        # Statistics tracking
        self.total_questions = 0
        self.total_correct = 0
        self.total_partial = 0
        self.total_incorrect = 0
        self.element_stats = {}  # Per-element type statistics

    def _normalize(self, text: str) -> str:
        """
        Normalize text for comparison.

        Args:
            text: Text to normalize

        Returns:
            Normalized text
        """
        if text is None:
            return ''

        # Convert to string
        text = str(text).strip()

        # Handle case sensitivity
        if not self.case_sensitive:
            text = text.upper()

        # Remove extra whitespace
        text = ' '.join(text.split())

        return text

    def _calculate_similarity(self, answer: str, correct: str) -> float:
        """
        Calculate similarity between two strings.

        Uses SequenceMatcher for Levenshtein-like similarity.

        Args:
            answer: User's answer
            correct: Correct answer

        Returns:
            Similarity ratio (0.0-1.0)
        """
        answer = self._normalize(answer)
        correct = self._normalize(correct)

        if not answer or not correct:
            return 0.0

        # Use SequenceMatcher for fuzzy matching
        return SequenceMatcher(None, answer, correct).ratio()

    def score_element(
        self,
        answer: str,
        correct: str,
        element_type: str = 'generic'
    ) -> Tuple[float, str]:
        """
        Score a single element with fuzzy matching.

        Args:
            answer: User's answer
            correct: Correct answer
            element_type: Type of element (for statistics)

        Returns:
            Tuple of (score, feedback):
                score: 0.0-1.0
                feedback: 'correct', 'partial', or 'incorrect'
        """
        # Normalize inputs
        answer_norm = self._normalize(answer)
        correct_norm = self._normalize(correct)

        # Empty answers are incorrect
        if not answer_norm:
            self._update_stats(element_type, 0.0, 'incorrect')
            return 0.0, 'incorrect'

        # Exact match
        if answer_norm == correct_norm:
            self._update_stats(element_type, 1.0, 'correct')
            return 1.0, 'correct'

        # Fuzzy matching
        if self.partial_credit:
            similarity = self._calculate_similarity(answer, correct)

            if similarity >= self.fuzzy_threshold:
                # Award partial credit based on similarity
                score = similarity
                self._update_stats(element_type, score, 'partial')
                return score, 'partial'

        # No match
        self._update_stats(element_type, 0.0, 'incorrect')
        return 0.0, 'incorrect'

    def score_callsign(self, answer: str, correct: str) -> Tuple[float, str]:
        """
        Score a callsign with strict matching.

        Callsigns use higher threshold for partial credit since they
        are critical identifiers.

        Args:
            answer: User's answer
            correct: Correct callsign

        Returns:
            Tuple of (score, feedback)
        """
        # Use stricter threshold for callsigns
        original_threshold = self.fuzzy_threshold
        self.fuzzy_threshold = max(0.9, self.fuzzy_threshold)

        result = self.score_element(answer, correct, 'callsign')

        # Restore original threshold
        self.fuzzy_threshold = original_threshold

        return result

    def score_rst(self, answer: str, correct: str) -> Tuple[float, str]:
        """
        Score an RST report.

        RST reports are 3-digit numbers (e.g., 599, 589).
        Partial credit awarded if 2 out of 3 digits match.

        Args:
            answer: User's answer
            correct: Correct RST

        Returns:
            Tuple of (score, feedback)
        """
        answer_norm = self._normalize(answer)
        correct_norm = self._normalize(correct)

        if not answer_norm:
            self._update_stats('rst', 0.0, 'incorrect')
            return 0.0, 'incorrect'

        # Exact match
        if answer_norm == correct_norm:
            self._update_stats('rst', 1.0, 'correct')
            return 1.0, 'correct'

        # Partial credit for RST
        if self.partial_credit and len(answer_norm) == 3 and len(correct_norm) == 3:
            matches = sum(a == c for a, c in zip(answer_norm, correct_norm))
            score = matches / 3.0

            if score >= 0.66:  # At least 2 out of 3 digits
                self._update_stats('rst', score, 'partial')
                return score, 'partial'

        self._update_stats('rst', 0.0, 'incorrect')
        return 0.0, 'incorrect'

    def score_qso(
        self,
        user_answers: Dict[str, str],
        correct_elements: Dict[str, List[str]]
    ) -> Dict:
        """
        Score a complete QSO.

        Args:
            user_answers: Dictionary of user answers
                {
                    'callsign1': 'W1ABC',
                    'callsign2': 'G3YWX',
                    'name1': 'BOB',
                    'name2': 'IAN',
                    'qth1': 'BOSTON',
                    'qth2': 'LONDON',
                    'rst1': '599',
                    'rst2': '589',
                    'rig1': 'IC7300',  # optional
                    'rig2': 'FT991A',  # optional
                    'antenna1': 'DIPOLE',  # optional
                    'antenna2': 'VERTICAL',  # optional
                    'power1': '100W',  # optional
                    'power2': '50W'  # optional
                }

            correct_elements: Dictionary from QSOGenerator.extract_qso_elements()
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
            Dictionary with scoring results:
            {
                'total_score': 18.5,
                'max_score': 21,
                'percentage': 88.1,
                'element_scores': {
                    'callsign1': {'score': 1.0, 'feedback': 'correct'},
                    'callsign2': {'score': 0.9, 'feedback': 'partial'},
                    ...
                },
                'summary': {
                    'correct': 15,
                    'partial': 3,
                    'incorrect': 3
                }
            }
        """
        element_scores = {}
        total_score = 0.0
        max_score = 0
        correct_count = 0
        partial_count = 0
        incorrect_count = 0

        # Define required elements
        required_elements = [
            ('callsign1', 'callsigns', 0, self.score_callsign),
            ('callsign2', 'callsigns', 1, self.score_callsign),
            ('name1', 'names', 0, self.score_element),
            ('name2', 'names', 1, self.score_element),
            ('qth1', 'qths', 0, self.score_element),
            ('qth2', 'qths', 1, self.score_element),
            ('rst1', 'rsts', 0, self.score_rst),
            ('rst2', 'rsts', 1, self.score_rst),
        ]

        # Optional elements
        optional_elements = [
            ('rig1', 'rigs', 0, self.score_element),
            ('rig2', 'rigs', 1, self.score_element),
            ('antenna1', 'antennas', 0, self.score_element),
            ('antenna2', 'antennas', 1, self.score_element),
            ('power1', 'powers', 0, self.score_element),
            ('power2', 'powers', 1, self.score_element),
        ]

        # Score required elements
        for key, element_type, index, score_func in required_elements:
            answer = user_answers.get(key, '')
            correct = correct_elements[element_type][index]

            score, feedback = score_func(answer, correct)

            element_scores[key] = {
                'score': score,
                'feedback': feedback,
                'correct': correct,
                'answer': answer
            }

            total_score += score
            max_score += 1

            if feedback == 'correct':
                correct_count += 1
            elif feedback == 'partial':
                partial_count += 1
            else:
                incorrect_count += 1

        # Score optional elements (only if provided in user answers)
        for key, element_type, index, score_func in optional_elements:
            if key in user_answers and user_answers[key]:
                answer = user_answers[key]
                correct = correct_elements[element_type][index]

                score, feedback = score_func(answer, correct)

                element_scores[key] = {
                    'score': score,
                    'feedback': feedback,
                    'correct': correct,
                    'answer': answer
                }

                total_score += score
                max_score += 1

                if feedback == 'correct':
                    correct_count += 1
                elif feedback == 'partial':
                    partial_count += 1
                else:
                    incorrect_count += 1

        # Calculate percentage
        percentage = (total_score / max_score * 100) if max_score > 0 else 0.0

        return {
            'total_score': round(total_score, 2),
            'max_score': max_score,
            'percentage': round(percentage, 1),
            'element_scores': element_scores,
            'summary': {
                'correct': correct_count,
                'partial': partial_count,
                'incorrect': incorrect_count
            }
        }

    def _update_stats(self, element_type: str, score: float, feedback: str):
        """Update internal statistics."""
        self.total_questions += 1

        if feedback == 'correct':
            self.total_correct += 1
        elif feedback == 'partial':
            self.total_partial += 1
        else:
            self.total_incorrect += 1

        # Per-element stats
        if element_type not in self.element_stats:
            self.element_stats[element_type] = {
                'total': 0,
                'correct': 0,
                'partial': 0,
                'incorrect': 0,
                'total_score': 0.0
            }

        stats = self.element_stats[element_type]
        stats['total'] += 1
        stats[feedback] += 1
        stats['total_score'] += score

    def get_statistics(self) -> Dict:
        """
        Get scoring statistics.

        Returns:
            Dictionary with overall and per-element statistics:
            {
                'overall': {
                    'total_questions': 150,
                    'correct': 120,
                    'partial': 20,
                    'incorrect': 10,
                    'accuracy': 80.0
                },
                'by_element': {
                    'callsign': {...},
                    'name': {...},
                    ...
                }
            }
        """
        overall_accuracy = (
            (self.total_correct / self.total_questions * 100)
            if self.total_questions > 0 else 0.0
        )

        # Calculate per-element statistics
        by_element = {}
        for element_type, stats in self.element_stats.items():
            total = stats['total']
            accuracy = (stats['correct'] / total * 100) if total > 0 else 0.0
            avg_score = (stats['total_score'] / total) if total > 0 else 0.0

            by_element[element_type] = {
                'total': total,
                'correct': stats['correct'],
                'partial': stats['partial'],
                'incorrect': stats['incorrect'],
                'accuracy': round(accuracy, 1),
                'average_score': round(avg_score, 2)
            }

        return {
            'overall': {
                'total_questions': self.total_questions,
                'correct': self.total_correct,
                'partial': self.total_partial,
                'incorrect': self.total_incorrect,
                'accuracy': round(overall_accuracy, 1)
            },
            'by_element': by_element
        }

    def reset_statistics(self):
        """Reset all statistics to zero."""
        self.total_questions = 0
        self.total_correct = 0
        self.total_partial = 0
        self.total_incorrect = 0
        self.element_stats = {}


class SessionScorer:
    """
    Tracks scoring across an entire practice session.

    Manages multiple QSO scores and provides session-level statistics.
    """

    def __init__(self, scorer: Optional[QSOScorer] = None):
        """
        Initialize session scorer.

        Args:
            scorer: QSOScorer instance (creates new one if None)
        """
        self.scorer = scorer if scorer else QSOScorer()
        self.qso_scores = []
        self.session_start_time = None
        self.session_end_time = None

    def add_qso_score(self, qso_result: Dict):
        """
        Add a QSO score to the session.

        Args:
            qso_result: Result from QSOScorer.score_qso()
        """
        self.qso_scores.append(qso_result)

    def get_session_summary(self) -> Dict:
        """
        Get summary of entire session.

        Returns:
            Dictionary with session statistics:
            {
                'qso_count': 5,
                'total_score': 92.5,
                'max_score': 105,
                'average_percentage': 88.1,
                'qso_scores': [...],
                'element_statistics': {...}
            }
        """
        if not self.qso_scores:
            return {
                'qso_count': 0,
                'total_score': 0,
                'max_score': 0,
                'average_percentage': 0.0,
                'qso_scores': [],
                'element_statistics': {}
            }

        total_score = sum(q['total_score'] for q in self.qso_scores)
        max_score = sum(q['max_score'] for q in self.qso_scores)
        average_percentage = (total_score / max_score * 100) if max_score > 0 else 0.0

        return {
            'qso_count': len(self.qso_scores),
            'total_score': round(total_score, 2),
            'max_score': max_score,
            'average_percentage': round(average_percentage, 1),
            'qso_scores': self.qso_scores,
            'element_statistics': self.scorer.get_statistics()
        }

    def get_qso_score(self, index: int) -> Optional[Dict]:
        """
        Get score for specific QSO.

        Args:
            index: QSO index (0-based)

        Returns:
            QSO score dictionary or None if index invalid
        """
        if 0 <= index < len(self.qso_scores):
            return self.qso_scores[index]
        return None

    def reset_session(self):
        """Reset session scores."""
        self.qso_scores = []
        self.scorer.reset_statistics()


# Module version
__version__ = '1.0.0'
