"""
Unit tests for QSO Data Module

Tests all data structures, validation functions, and sanitization logic
in the qso_data module.

Author: Generated with Claude Code
Date: 2025-11-28
Issue: #2 - QSO Feature: Data Module Foundation
"""

import unittest
import logging
import qso_data


class TestAbbreviationDictionary(unittest.TestCase):
    """Test the abbreviation dictionary structure and content."""

    def test_abbreviations_exist(self):
        """Test that abbreviation dictionary is loaded."""
        self.assertIsInstance(qso_data.ABBREVIATIONS, dict)
        self.assertGreater(len(qso_data.ABBREVIATIONS), 0)

    def test_common_abbreviations_present(self):
        """Test that essential abbreviations are present."""
        essential = ['GM', 'OM', 'TNX', 'FB', 'QTH', '73', 'CQ', 'DE', 'K']
        for abbr in essential:
            self.assertIn(abbr, qso_data.ABBREVIATIONS)
            self.assertIsInstance(qso_data.ABBREVIATIONS[abbr], str)
            self.assertGreater(len(qso_data.ABBREVIATIONS[abbr]), 0)

    def test_abbreviation_categories(self):
        """Test that abbreviation categories are properly defined."""
        self.assertIsInstance(qso_data.ABBREVIATION_CATEGORIES, dict)

        # Check required categories exist
        required_categories = ['greetings', 'friendly', 'q_codes', 'prosigns']
        for category in required_categories:
            self.assertIn(category, qso_data.ABBREVIATION_CATEGORIES)
            self.assertIsInstance(qso_data.ABBREVIATION_CATEGORIES[category], list)

    def test_abbreviations_are_uppercase(self):
        """Test that all abbreviation keys are uppercase."""
        for abbr in qso_data.ABBREVIATIONS.keys():
            self.assertEqual(abbr, abbr.upper(), f"Abbreviation '{abbr}' should be uppercase")


class TestOperatorNames(unittest.TestCase):
    """Test operator names data."""

    def test_names_exist(self):
        """Test that name list is loaded."""
        self.assertIsInstance(qso_data.COMMON_NAMES, list)
        self.assertGreater(len(qso_data.COMMON_NAMES), 0)

    def test_names_are_uppercase(self):
        """Test that all names are uppercase."""
        for name in qso_data.COMMON_NAMES:
            self.assertEqual(name, name.upper(), f"Name '{name}' should be uppercase")

    def test_names_are_strings(self):
        """Test that all names are strings."""
        for name in qso_data.COMMON_NAMES:
            self.assertIsInstance(name, str)
            self.assertGreater(len(name), 0)

    def test_no_duplicate_names(self):
        """Test that there are no duplicate names."""
        self.assertEqual(len(qso_data.COMMON_NAMES), len(set(qso_data.COMMON_NAMES)))


class TestGeographicLocations(unittest.TestCase):
    """Test geographic location data (QTH)."""

    def test_city_lists_exist(self):
        """Test that all city lists are loaded."""
        city_lists = [
            qso_data.US_CITIES,
            qso_data.UK_CITIES,
            qso_data.EU_CITIES,
            qso_data.GERMAN_CITIES,
            qso_data.FRENCH_CITIES,
            qso_data.ITALIAN_CITIES,
            qso_data.BELGIAN_CITIES,
            qso_data.DUTCH_CITIES,
            qso_data.SPANISH_CITIES,
            qso_data.ASIA_PACIFIC_CITIES,
            qso_data.ALL_CITIES,
        ]

        for city_list in city_lists:
            self.assertIsInstance(city_list, list)
            self.assertGreater(len(city_list), 0)

    def test_cities_are_uppercase(self):
        """Test that all cities are uppercase."""
        for city in qso_data.ALL_CITIES:
            self.assertEqual(city, city.upper(), f"City '{city}' should be uppercase")

    def test_cities_by_region_structure(self):
        """Test CITIES_BY_REGION dictionary structure."""
        self.assertIsInstance(qso_data.CITIES_BY_REGION, dict)

        expected_regions = ['us', 'uk', 'germany', 'france', 'italy',
                           'belgium', 'netherlands', 'spain', 'asia_pacific']
        for region in expected_regions:
            self.assertIn(region, qso_data.CITIES_BY_REGION)
            self.assertIsInstance(qso_data.CITIES_BY_REGION[region], list)

    def test_all_cities_count(self):
        """Test that ALL_CITIES contains expected number of cities."""
        # ALL_CITIES should equal US + UK + EU + Asia/Pacific
        expected_count = (len(qso_data.US_CITIES) +
                         len(qso_data.UK_CITIES) +
                         len(qso_data.EU_CITIES) +
                         len(qso_data.ASIA_PACIFIC_CITIES))
        self.assertEqual(len(qso_data.ALL_CITIES), expected_count)


class TestRadioEquipment(unittest.TestCase):
    """Test radio equipment data."""

    def test_transceiver_lists_exist(self):
        """Test that transceiver lists are loaded."""
        transceiver_lists = [
            qso_data.ICOM_RIGS,
            qso_data.YAESU_RIGS,
            qso_data.KENWOOD_RIGS,
            qso_data.ELECRAFT_RIGS,
            qso_data.TRANSCEIVERS,
        ]

        for rig_list in transceiver_lists:
            self.assertIsInstance(rig_list, list)
            self.assertGreater(len(rig_list), 0)

    def test_transceivers_are_uppercase(self):
        """Test that all transceiver names are uppercase."""
        for rig in qso_data.TRANSCEIVERS:
            self.assertEqual(rig, rig.upper(), f"Transceiver '{rig}' should be uppercase")

    def test_antennas_exist(self):
        """Test that antenna list is loaded."""
        self.assertIsInstance(qso_data.ANTENNAS, list)
        self.assertGreater(len(qso_data.ANTENNAS), 10)

    def test_power_levels_exist(self):
        """Test that power levels list is loaded."""
        self.assertIsInstance(qso_data.POWER_LEVELS, list)
        self.assertGreater(len(qso_data.POWER_LEVELS), 0)

    def test_power_levels_format(self):
        """Test that power levels are correctly formatted."""
        for power in qso_data.POWER_LEVELS:
            self.assertRegex(power, r'^\d+W$', f"Power '{power}' should be in format 'NW'")

    def test_equipment_by_type_structure(self):
        """Test EQUIPMENT_BY_TYPE dictionary structure."""
        self.assertIsInstance(qso_data.EQUIPMENT_BY_TYPE, dict)

        expected_types = ['icom', 'yaesu', 'kenwood', 'elecraft']
        for eq_type in expected_types:
            self.assertIn(eq_type, qso_data.EQUIPMENT_BY_TYPE)
            self.assertIsInstance(qso_data.EQUIPMENT_BY_TYPE[eq_type], list)


class TestEnvironmentalData(unittest.TestCase):
    """Test weather and environmental data."""

    def test_weather_conditions_exist(self):
        """Test that weather conditions list is loaded."""
        self.assertIsInstance(qso_data.WEATHER_CONDITIONS, list)
        self.assertGreater(len(qso_data.WEATHER_CONDITIONS), 0)

    def test_temperatures_exist(self):
        """Test that temperature list is loaded."""
        self.assertIsInstance(qso_data.TEMPERATURES, list)
        self.assertGreater(len(qso_data.TEMPERATURES), 0)

    def test_temperature_format(self):
        """Test that temperatures are correctly formatted."""
        for temp in qso_data.TEMPERATURES:
            self.assertRegex(temp, r'^-?\d+C$', f"Temperature '{temp}' should be in format 'NC'")


class TestSignalReports(unittest.TestCase):
    """Test signal report (RST) data."""

    def test_rst_reports_exist(self):
        """Test that RST reports list is loaded."""
        self.assertIsInstance(qso_data.RST_REPORTS, list)
        self.assertGreater(len(qso_data.RST_REPORTS), 0)

    def test_rst_format(self):
        """Test that RST reports are correctly formatted."""
        for rst in qso_data.RST_REPORTS:
            self.assertRegex(rst, r'^[1-5][1-9][1-9]$',
                           f"RST '{rst}' should be 3 digits (R:1-5, S:1-9, T:1-9)")

    def test_common_rst_values_present(self):
        """Test that common RST values are present."""
        common_rst = ['599', '589', '579']
        for rst in common_rst:
            self.assertIn(rst, qso_data.RST_REPORTS)


class TestValidateNameFunction(unittest.TestCase):
    """Test the validate_name() function."""

    def test_valid_names(self):
        """Test validation of valid names."""
        valid_names = ['BOB', 'JOHN', 'MARY', 'ANNA', 'HANS']
        for name in valid_names:
            self.assertTrue(qso_data.validate_name(name),
                          f"'{name}' should be valid")

    def test_invalid_names(self):
        """Test rejection of invalid names."""
        invalid_names = [
            '',                      # Empty
            'bob',                   # Lowercase
            '123',                   # Numbers only
            'BOB123',                # Contains numbers
            'A',                     # Too short (less than 2 chars)
            'A' * 50,                # Too long
            'BOB<SCRIPT>',           # Injection attempt
            'BOB; DROP TABLE',       # SQL injection attempt
            None,                    # None type
            123,                     # Wrong type
        ]

        for name in invalid_names:
            self.assertFalse(qso_data.validate_name(name),
                           f"'{name}' should be invalid")

    def test_name_with_spaces(self):
        """Test names with spaces."""
        # Multi-word names are allowed by the validation (though not in our list)
        # The regex permits spaces: r'^[A-Z][A-Z\s]{1,19}$'
        # This is intentional to support flexibility
        self.assertTrue(qso_data.validate_name('BOB SMITH'),
                       'Names with spaces should be valid per regex pattern')


class TestValidateQTHFunction(unittest.TestCase):
    """Test the validate_qth() function."""

    def test_valid_qth(self):
        """Test validation of valid locations."""
        valid_qth = ['BOSTON', 'LONDON', 'BERLIN', 'NEW YORK', 'LOS ANGELES']
        for qth in valid_qth:
            self.assertTrue(qso_data.validate_qth(qth),
                          f"'{qth}' should be valid")

    def test_invalid_qth(self):
        """Test rejection of invalid locations."""
        invalid_qth = [
            '',                      # Empty
            'boston',                # Lowercase
            '---',                   # Invalid characters
            'A',                     # Too short
            'X' * 100,               # Too long
            'BOSTON123',             # Contains numbers
            None,                    # None type
            123,                     # Wrong type
        ]

        for qth in invalid_qth:
            self.assertFalse(qso_data.validate_qth(qth),
                           f"'{qth}' should be invalid")


class TestValidateRSTFunction(unittest.TestCase):
    """Test the validate_rst() function."""

    def test_valid_rst(self):
        """Test validation of valid RST reports."""
        valid_rst = ['599', '589', '579', '569', '559', '549', '539', '449', '119']
        for rst in valid_rst:
            self.assertTrue(qso_data.validate_rst(rst),
                          f"'{rst}' should be valid")

    def test_invalid_rst(self):
        """Test rejection of invalid RST reports."""
        invalid_rst = [
            '',                      # Empty
            '99',                    # Too short
            '5999',                  # Too long
            '000',                   # Invalid values (0s)
            '999',                   # Invalid readability (9)
            '699',                   # Invalid readability (6)
            '590',                   # Invalid strength (0)
            '500',                   # Invalid tone (0)
            'ABC',                   # Letters
            '59',                    # Missing digit
            None,                    # None type
            599,                     # Wrong type (int instead of string)
        ]

        for rst in invalid_rst:
            self.assertFalse(qso_data.validate_rst(rst),
                           f"'{rst}' should be invalid")


class TestValidateEquipmentFunction(unittest.TestCase):
    """Test the validate_equipment() function."""

    def test_valid_equipment(self):
        """Test validation of valid equipment names."""
        valid_equipment = ['IC7300', 'FT991A', 'DIPOLE', 'YAGI', 'BEAM', 'K3']
        for equipment in valid_equipment:
            self.assertTrue(qso_data.validate_equipment(equipment),
                          f"'{equipment}' should be valid")

    def test_invalid_equipment(self):
        """Test rejection of invalid equipment."""
        invalid_equipment = [
            '',                      # Empty
            'ic7300',                # Lowercase
            'X',                     # Too short
            'A' * 100,               # Too long
            'RIG<SCRIPT>',           # Injection attempt
            None,                    # None type
            123,                     # Wrong type
        ]

        for equipment in invalid_equipment:
            self.assertFalse(qso_data.validate_equipment(equipment),
                           f"'{equipment}' should be invalid")


class TestValidatePowerFunction(unittest.TestCase):
    """Test the validate_power() function."""

    def test_valid_power(self):
        """Test validation of valid power levels."""
        valid_power = ['5W', '10W', '50W', '100W', '500W', '1000W', '1500W']
        for power in valid_power:
            self.assertTrue(qso_data.validate_power(power),
                          f"'{power}' should be valid")

    def test_invalid_power(self):
        """Test rejection of invalid power levels."""
        invalid_power = [
            '',                      # Empty
            '100',                   # Missing 'W'
            'W100',                  # Wrong format
            '100w',                  # Lowercase
            '0W',                    # Too low
            '2000W',                 # Too high (above amateur radio limits)
            'ABCW',                  # Letters
            '100 W',                 # Space
            None,                    # None type
            100,                     # Wrong type
        ]

        for power in invalid_power:
            self.assertFalse(qso_data.validate_power(power),
                           f"'{power}' should be invalid")


class TestSanitizeTextFunction(unittest.TestCase):
    """Test the sanitize_text() function."""

    def test_basic_sanitization(self):
        """Test basic text sanitization."""
        test_cases = [
            ('hello world', 'HELLO WORLD'),
            ('TEST 123', 'TEST 123'),
            ('lower case', 'LOWER CASE'),
        ]

        for input_text, expected in test_cases:
            result = qso_data.sanitize_text(input_text)
            self.assertEqual(result, expected,
                           f"sanitize_text('{input_text}') should return '{expected}'")

    def test_sanitization_removes_dangerous_chars(self):
        """Test that sanitization removes dangerous characters."""
        dangerous_inputs = [
            'hello<script>alert()</script>',
            'test\x00null\x00bytes',
            'hello;DROP TABLE users',
            'test\nwith\nnewlines',
            'test\twith\ttabs',
        ]

        for dangerous_input in dangerous_inputs:
            result = qso_data.sanitize_text(dangerous_input)
            # Should not contain any dangerous characters
            self.assertNotRegex(result, r'[<>;\x00\n\r\t]',
                              f"Sanitized text should not contain dangerous characters")

    def test_sanitization_length_limit(self):
        """Test that sanitization enforces length limits."""
        long_text = 'A' * 200
        result = qso_data.sanitize_text(long_text, max_length=50)
        self.assertEqual(len(result), 50, "Sanitized text should be truncated to max_length")

    def test_sanitization_empty_input(self):
        """Test sanitization of empty input."""
        self.assertEqual(qso_data.sanitize_text(''), '')

    def test_sanitization_preserves_allowed_chars(self):
        """Test that sanitization preserves allowed characters."""
        allowed_text = 'ABC123 XYZ-789/TEST'
        result = qso_data.sanitize_text(allowed_text)
        self.assertEqual(result, allowed_text)

    def test_sanitization_wrong_type(self):
        """Test sanitization handles wrong input types."""
        result = qso_data.sanitize_text(None)
        self.assertEqual(result, '')

        result = qso_data.sanitize_text(123)
        self.assertEqual(result, '')


class TestModuleStructure(unittest.TestCase):
    """Test module structure and exports."""

    def test_public_api_exports(self):
        """Test that __all__ is properly defined."""
        self.assertIsInstance(qso_data.__all__, list)
        self.assertGreater(len(qso_data.__all__), 0)

    def test_exported_items_exist(self):
        """Test that all exported items actually exist in module."""
        for item in qso_data.__all__:
            self.assertTrue(hasattr(qso_data, item),
                          f"Exported item '{item}' should exist in module")

    def test_module_metadata(self):
        """Test that module metadata is present."""
        self.assertTrue(hasattr(qso_data, '__version__'))
        self.assertTrue(hasattr(qso_data, '__author__'))
        self.assertTrue(hasattr(qso_data, '__date__'))


class TestDataIntegrity(unittest.TestCase):
    """Test overall data integrity and consistency."""

    def test_no_empty_lists(self):
        """Test that no data lists are empty."""
        data_lists = [
            ('ABBREVIATIONS', qso_data.ABBREVIATIONS),
            ('COMMON_NAMES', qso_data.COMMON_NAMES),
            ('US_CITIES', qso_data.US_CITIES),
            ('TRANSCEIVERS', qso_data.TRANSCEIVERS),
            ('ANTENNAS', qso_data.ANTENNAS),
            ('POWER_LEVELS', qso_data.POWER_LEVELS),
            ('WEATHER_CONDITIONS', qso_data.WEATHER_CONDITIONS),
            ('TEMPERATURES', qso_data.TEMPERATURES),
            ('RST_REPORTS', qso_data.RST_REPORTS),
        ]

        for name, data_list in data_lists:
            self.assertGreater(len(data_list), 0, f"{name} should not be empty")

    def test_data_types_consistency(self):
        """Test that data types are consistent within lists."""
        # All items in name list should be strings
        for name in qso_data.COMMON_NAMES:
            self.assertIsInstance(name, str)

        # All items in city lists should be strings
        for city in qso_data.ALL_CITIES:
            self.assertIsInstance(city, str)

        # All items in equipment lists should be strings
        for rig in qso_data.TRANSCEIVERS:
            self.assertIsInstance(rig, str)


def run_tests():
    """Run all tests and return results."""
    # Suppress logging during tests
    logging.disable(logging.CRITICAL)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Re-enable logging
    logging.disable(logging.NOTSET)

    return result


if __name__ == '__main__':
    result = run_tests()

    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
