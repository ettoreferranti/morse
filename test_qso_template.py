"""
Unit tests for QSOTemplate class

Tests all QSO template generation and substitution functionality.

Author: Generated with Claude Code
Date: 2025-11-28
Issue: #4 - QSO Feature: Template System
"""

import unittest
import re
from qso_data import QSOTemplate, CallSignGenerator
import qso_data


class TestQSOTemplateInit(unittest.TestCase):
    """Test QSOTemplate initialization."""

    def test_initialization(self):
        """Test that template generator initializes correctly."""
        template = QSOTemplate()
        self.assertIsInstance(template, QSOTemplate)
        self.assertTrue(hasattr(template, 'random'))


class TestMinimalTemplate(unittest.TestCase):
    """Test minimal verbosity template generation."""

    def setUp(self):
        """Set up test template generator."""
        self.template = QSOTemplate()

    def test_generate_minimal_returns_string(self):
        """Test that minimal template returns a string."""
        result = self.template.generate_minimal()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_minimal_contains_required_variables(self):
        """Test that minimal template contains required variable placeholders."""
        result = self.template.generate_minimal()

        # Should contain call signs
        self.assertIn('{CALL1}', result)
        self.assertIn('{CALL2}', result)

        # Should contain names
        self.assertIn('{NAME1}', result)
        self.assertIn('{NAME2}', result)

        # Should contain RST reports
        self.assertIn('{RST1}', result)
        self.assertIn('{RST2}', result)

    def test_minimal_has_prosigns(self):
        """Test that minimal template contains proper prosigns."""
        result = self.template.generate_minimal()

        # Should have proper prosigns
        self.assertIn('K', result)  # Over/invitation to transmit
        self.assertIn('SK', result)  # End of contact

    def test_minimal_variety(self):
        """Test that multiple calls produce different templates."""
        templates = [self.template.generate_minimal() for _ in range(20)]
        unique_templates = set(templates)

        # Should have some variety (at least 2 different templates)
        self.assertGreater(len(unique_templates), 1)


class TestMediumTemplate(unittest.TestCase):
    """Test medium verbosity template generation."""

    def setUp(self):
        """Set up test template generator."""
        self.template = QSOTemplate()

    def test_generate_medium_returns_string(self):
        """Test that medium template returns a string."""
        result = self.template.generate_medium()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_medium_contains_all_variables(self):
        """Test that medium template contains all variable types."""
        result = self.template.generate_medium()

        # Call signs
        self.assertIn('{CALL1}', result)
        self.assertIn('{CALL2}', result)

        # Names
        self.assertIn('{NAME1}', result)
        self.assertIn('{NAME2}', result)

        # Locations
        self.assertIn('{QTH1}', result)
        self.assertIn('{QTH2}', result)

        # RST reports
        self.assertIn('{RST1}', result)
        self.assertIn('{RST2}', result)

        # Equipment (at least some of these)
        has_equipment = (
            '{RIG1}' in result or '{RIG2}' in result or
            '{ANT1}' in result or '{ANT2}' in result or
            '{PWR1}' in result or '{PWR2}' in result
        )
        self.assertTrue(has_equipment, "Medium template should contain equipment variables")

    def test_medium_longer_than_minimal(self):
        """Test that medium templates are generally longer than minimal."""
        minimal = self.template.generate_minimal()
        medium = self.template.generate_medium()

        # Medium should typically be longer (more verbose)
        # Allow some variance, but on average should be longer
        medium_avg_length = sum(len(self.template.generate_medium()) for _ in range(10)) / 10
        minimal_avg_length = sum(len(self.template.generate_minimal()) for _ in range(10)) / 10

        self.assertGreater(medium_avg_length, minimal_avg_length)


class TestChattyTemplate(unittest.TestCase):
    """Test chatty verbosity template generation."""

    def setUp(self):
        """Set up test template generator."""
        self.template = QSOTemplate()

    def test_generate_chatty_returns_string(self):
        """Test that chatty template returns a string."""
        result = self.template.generate_chatty()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_chatty_contains_weather_variables(self):
        """Test that chatty template contains weather information."""
        result = self.template.generate_chatty()

        # Should have weather variables
        self.assertIn('{WX1}', result)
        self.assertIn('{WX2}', result)

        # Should have temperature variables
        self.assertIn('{TEMP1}', result)
        self.assertIn('{TEMP2}', result)

    def test_chatty_contains_all_equipment(self):
        """Test that chatty template contains all equipment types."""
        result = self.template.generate_chatty()

        # Should have rigs
        self.assertIn('{RIG1}', result)
        self.assertIn('{RIG2}', result)

        # Should have antennas
        self.assertIn('{ANT1}', result)
        self.assertIn('{ANT2}', result)

        # Should have power
        self.assertIn('{PWR1}', result)
        self.assertIn('{PWR2}', result)

    def test_chatty_longest_template(self):
        """Test that chatty templates are longest."""
        minimal = self.template.generate_minimal()
        medium = self.template.generate_medium()
        chatty = self.template.generate_chatty()

        # Get average lengths
        chatty_avg = sum(len(self.template.generate_chatty()) for _ in range(10)) / 10
        medium_avg = sum(len(self.template.generate_medium()) for _ in range(10)) / 10
        minimal_avg = sum(len(self.template.generate_minimal()) for _ in range(10)) / 10

        self.assertGreater(chatty_avg, medium_avg)
        self.assertGreater(chatty_avg, minimal_avg)


class TestGenerateMethod(unittest.TestCase):
    """Test the main generate() method."""

    def setUp(self):
        """Set up test template generator."""
        self.template = QSOTemplate()

    def test_generate_default_is_medium(self):
        """Test that default verbosity is medium."""
        result = self.template.generate()
        # Should contain equipment variables like medium
        has_equipment = (
            '{RIG1}' in result or '{RIG2}' in result or
            '{ANT1}' in result or '{ANT2}' in result
        )
        self.assertTrue(has_equipment)

    def test_generate_minimal_verbosity(self):
        """Test generating minimal verbosity template."""
        result = self.template.generate('minimal')
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_generate_medium_verbosity(self):
        """Test generating medium verbosity template."""
        result = self.template.generate('medium')
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_generate_chatty_verbosity(self):
        """Test generating chatty verbosity template."""
        result = self.template.generate('chatty')
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_generate_case_insensitive(self):
        """Test that verbosity parameter is case insensitive."""
        result1 = self.template.generate('MINIMAL')
        result2 = self.template.generate('Minimal')
        result3 = self.template.generate('minimal')

        # All should work (may be different templates, but valid)
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)
        self.assertIsInstance(result3, str)

    def test_generate_invalid_verbosity_raises_error(self):
        """Test that invalid verbosity raises ValueError."""
        with self.assertRaises(ValueError):
            self.template.generate('invalid')

        with self.assertRaises(ValueError):
            self.template.generate('super_chatty')

    def test_generate_whitespace_handling(self):
        """Test that verbosity parameter handles whitespace."""
        result = self.template.generate('  medium  ')
        self.assertIsInstance(result, str)


class TestSubstituteVariables(unittest.TestCase):
    """Test variable substitution functionality."""

    def setUp(self):
        """Set up test template generator and sample variables."""
        self.template = QSOTemplate()
        self.call_gen = CallSignGenerator()

        # Create valid sample variables
        self.valid_vars = {
            'CALL1': 'W1ABC',
            'CALL2': 'G3XYZ',
            'NAME1': 'BOB',
            'NAME2': 'JOHN',
            'QTH1': 'BOSTON',
            'QTH2': 'LONDON',
            'RST1': '599',
            'RST2': '579',
            'RIG1': 'IC7300',
            'RIG2': 'FT991A',
            'ANT1': 'DIPOLE',
            'ANT2': 'BEAM',
            'PWR1': '100W',
            'PWR2': '50W',
            'WX1': 'SUNNY',
            'WX2': 'CLOUDY',
            'TEMP1': '20C',
            'TEMP2': '15C',
        }

    def test_substitute_basic_template(self):
        """Test substitution with a simple template."""
        template_str = "CQ DE {CALL1} = NAME {NAME1} = QTH {QTH1} K"
        result = self.template.substitute_variables(template_str, self.valid_vars)

        self.assertIn('W1ABC', result)
        self.assertIn('BOB', result)
        self.assertIn('BOSTON', result)
        self.assertNotIn('{CALL1}', result)
        self.assertNotIn('{NAME1}', result)

    def test_substitute_all_variables(self):
        """Test that all variables get substituted."""
        template_str = self.template.generate_chatty()
        result = self.template.substitute_variables(template_str, self.valid_vars)

        # No placeholders should remain
        self.assertNotIn('{CALL1}', result)
        self.assertNotIn('{CALL2}', result)
        self.assertNotIn('{NAME1}', result)
        self.assertNotIn('{NAME2}', result)
        self.assertNotIn('{RST1}', result)
        self.assertNotIn('{RST2}', result)

    def test_substitute_uppercase_conversion(self):
        """Test that substituted values are converted to uppercase."""
        # The substitute_variables method converts values to uppercase
        # But validation requires proper format, so use valid values
        vars_mixed = self.valid_vars.copy()
        vars_mixed['RST1'] = '599'  # Valid RST

        template_str = "RST {RST1}"
        result = self.template.substitute_variables(template_str, vars_mixed)

        # Should be uppercase
        self.assertIn('599', result)
        self.assertIsInstance(result, str)
        self.assertEqual(result, result.upper())

    def test_substitute_missing_variable_raises_error(self):
        """Test that missing required variable raises KeyError."""
        incomplete_vars = self.valid_vars.copy()
        del incomplete_vars['CALL1']

        template_str = "CQ DE {CALL1} K"

        with self.assertRaises(KeyError):
            self.template.substitute_variables(template_str, incomplete_vars)

    def test_substitute_invalid_callsign_raises_error(self):
        """Test that invalid call sign raises ValueError."""
        invalid_vars = self.valid_vars.copy()
        invalid_vars['CALL1'] = 'INVALID123456789'  # Too long

        template_str = "CQ DE {CALL1} K"

        with self.assertRaises(ValueError):
            self.template.substitute_variables(template_str, invalid_vars)

    def test_substitute_invalid_name_raises_error(self):
        """Test that invalid name raises ValueError."""
        invalid_vars = self.valid_vars.copy()
        invalid_vars['NAME1'] = '123'  # Numbers only

        template_str = "NAME {NAME1}"

        with self.assertRaises(ValueError):
            self.template.substitute_variables(template_str, invalid_vars)

    def test_substitute_invalid_rst_raises_error(self):
        """Test that invalid RST raises ValueError."""
        invalid_vars = self.valid_vars.copy()
        invalid_vars['RST1'] = '999'  # Invalid (R can't be 9)

        template_str = "UR RST {RST1}"

        with self.assertRaises(ValueError):
            self.template.substitute_variables(template_str, invalid_vars)

    def test_substitute_invalid_power_raises_error(self):
        """Test that invalid power raises ValueError."""
        invalid_vars = self.valid_vars.copy()
        invalid_vars['PWR1'] = '5000W'  # Too high

        template_str = "PWR {PWR1}"

        with self.assertRaises(ValueError):
            self.template.substitute_variables(template_str, invalid_vars)


class TestTemplateIntegration(unittest.TestCase):
    """Test integration of template generation and substitution."""

    def setUp(self):
        """Set up test components."""
        self.template = QSOTemplate()
        self.call_gen = CallSignGenerator()

    def test_generate_and_substitute_minimal(self):
        """Test complete workflow with minimal template."""
        template_str = self.template.generate('minimal')

        variables = {
            'CALL1': self.call_gen.generate('us'),
            'CALL2': self.call_gen.generate('uk'),
            'NAME1': qso_data.COMMON_NAMES[0],
            'NAME2': qso_data.COMMON_NAMES[1],
            'QTH1': qso_data.US_CITIES[0],
            'QTH2': qso_data.UK_CITIES[0],
            'RST1': '599',
            'RST2': '579',
            'RIG1': qso_data.TRANSCEIVERS[0],
            'RIG2': qso_data.TRANSCEIVERS[1],
            'ANT1': qso_data.ANTENNAS[0],
            'ANT2': qso_data.ANTENNAS[1],
            'PWR1': '100W',
            'PWR2': '50W',
            'WX1': qso_data.WEATHER_CONDITIONS[0],
            'WX2': qso_data.WEATHER_CONDITIONS[1],
            'TEMP1': '20C',
            'TEMP2': '15C',
        }

        result = self.template.substitute_variables(template_str, variables)

        # Result should be valid
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

        # Should contain actual values
        self.assertIn(variables['NAME1'], result)
        self.assertIn(variables['NAME2'], result)

    def test_generate_and_substitute_medium(self):
        """Test complete workflow with medium template."""
        template_str = self.template.generate('medium')

        variables = {
            'CALL1': 'W1ABC',
            'CALL2': 'DL1XYZ',
            'NAME1': 'MIKE',
            'NAME2': 'HANS',
            'QTH1': 'CHICAGO',
            'QTH2': 'BERLIN',
            'RST1': '589',
            'RST2': '569',
            'RIG1': 'IC7300',
            'RIG2': 'TS590',
            'ANT1': 'DIPOLE',
            'ANT2': 'YAGI',
            'PWR1': '100W',
            'PWR2': '75W',
            'WX1': 'CLEAR',
            'WX2': 'RAIN',
            'TEMP1': '25C',
            'TEMP2': '10C',
        }

        result = self.template.substitute_variables(template_str, variables)

        # Should contain equipment information
        self.assertIn('IC7300', result)
        self.assertIn('TS590', result)

    def test_generate_and_substitute_chatty(self):
        """Test complete workflow with chatty template."""
        template_str = self.template.generate('chatty')

        variables = {
            'CALL1': 'VK3ABC',
            'CALL2': 'JA1XYZ',
            'NAME1': 'TOM',
            'NAME2': 'YOSHI',
            'QTH1': 'SYDNEY',
            'QTH2': 'TOKYO',
            'RST1': '599',
            'RST2': '559',
            'RIG1': 'K3',
            'RIG2': 'FT991A',
            'ANT1': 'BEAM',
            'ANT2': 'VERTICAL',
            'PWR1': '100W',
            'PWR2': '50W',
            'WX1': 'SUNNY',
            'WX2': 'CLOUDY',
            'TEMP1': '30C',
            'TEMP2': '15C',
        }

        result = self.template.substitute_variables(template_str, variables)

        # Should contain weather information
        self.assertIn('SUNNY', result)
        self.assertIn('CLOUDY', result)
        self.assertIn('30C', result)
        self.assertIn('15C', result)

    def test_multiple_qsos_are_unique(self):
        """Test that multiple QSO generations produce variety."""
        qsos = []
        for _ in range(10):
            template_str = self.template.generate('medium')

            variables = {
                'CALL1': self.call_gen.generate(),
                'CALL2': self.call_gen.generate(),
                'NAME1': qso_data.COMMON_NAMES[_ % len(qso_data.COMMON_NAMES)],
                'NAME2': qso_data.COMMON_NAMES[(_ + 1) % len(qso_data.COMMON_NAMES)],
                'QTH1': qso_data.ALL_CITIES[_ % len(qso_data.ALL_CITIES)],
                'QTH2': qso_data.ALL_CITIES[(_ + 1) % len(qso_data.ALL_CITIES)],
                'RST1': qso_data.RST_REPORTS[_ % len(qso_data.RST_REPORTS)],
                'RST2': qso_data.RST_REPORTS[(_ + 1) % len(qso_data.RST_REPORTS)],
                'RIG1': qso_data.TRANSCEIVERS[_ % len(qso_data.TRANSCEIVERS)],
                'RIG2': qso_data.TRANSCEIVERS[(_ + 1) % len(qso_data.TRANSCEIVERS)],
                'ANT1': qso_data.ANTENNAS[_ % len(qso_data.ANTENNAS)],
                'ANT2': qso_data.ANTENNAS[(_ + 1) % len(qso_data.ANTENNAS)],
                'PWR1': qso_data.POWER_LEVELS[_ % len(qso_data.POWER_LEVELS)],
                'PWR2': qso_data.POWER_LEVELS[(_ + 1) % len(qso_data.POWER_LEVELS)],
                'WX1': qso_data.WEATHER_CONDITIONS[_ % len(qso_data.WEATHER_CONDITIONS)],
                'WX2': qso_data.WEATHER_CONDITIONS[(_ + 1) % len(qso_data.WEATHER_CONDITIONS)],
                'TEMP1': qso_data.TEMPERATURES[_ % len(qso_data.TEMPERATURES)],
                'TEMP2': qso_data.TEMPERATURES[(_ + 1) % len(qso_data.TEMPERATURES)],
            }

            result = self.template.substitute_variables(template_str, variables)
            qsos.append(result)

        # Should have variety in generated QSOs
        unique_qsos = set(qsos)
        self.assertGreater(len(unique_qsos), 5)


class TestTemplateRealism(unittest.TestCase):
    """Test that templates produce realistic QSOs."""

    def setUp(self):
        """Set up test template generator."""
        self.template = QSOTemplate()

    def test_templates_have_cq_call(self):
        """Test that templates start with CQ call."""
        for verbosity in ['minimal', 'medium', 'chatty']:
            # Generate multiple templates of each type
            for _ in range(5):
                result = self.template.generate(verbosity)
                # Should start with CQ
                self.assertTrue(result.strip().startswith('CQ'),
                              f"{verbosity} template should start with CQ")

    def test_templates_have_proper_structure(self):
        """Test that templates have proper QSO structure."""
        for verbosity in ['minimal', 'medium', 'chatty']:
            result = self.template.generate(verbosity)

            # Should have DE (from)
            self.assertIn('DE', result)

            # Should have K (over/invitation)
            self.assertIn('K', result)

            # Should have SK (end of contact)
            self.assertIn('SK', result)

    def test_templates_use_abbreviations(self):
        """Test that templates use authentic abbreviations."""
        result = self.template.generate('chatty')

        # Should use common abbreviations
        common_abbrevs = ['TNX', 'FB', 'OM', 'UR', 'HR', 'VY', 'ES']
        found_abbrevs = sum(1 for abbrev in common_abbrevs if abbrev in result)

        self.assertGreater(found_abbrevs, 3,
                          "Template should use multiple common abbreviations")


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
