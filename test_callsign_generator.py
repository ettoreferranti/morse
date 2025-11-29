"""
Unit tests for CallSignGenerator class

Tests all call sign generation functionality for multiple regions.

Author: Generated with Claude Code
Date: 2025-11-28
Issue: #3 - QSO Feature: Call Sign Generator
"""

import unittest
import re
from qso_data import CallSignGenerator


class TestCallSignGeneratorInit(unittest.TestCase):
    """Test CallSignGenerator initialization."""

    def test_initialization(self):
        """Test that generator initializes correctly."""
        gen = CallSignGenerator()
        self.assertIsInstance(gen, CallSignGenerator)

    def test_has_required_attributes(self):
        """Test that generator has all required pattern attributes."""
        gen = CallSignGenerator()

        required_attrs = [
            'us_prefixes_1', 'us_prefixes_2', 'us_regions',
            'uk_prefixes', 'uk_regions',
            'german_prefixes', 'german_regions',
            'french_regions', 'italian_regions',
            'belgian_regions', 'dutch_prefixes', 'dutch_regions',
            'spanish_prefixes', 'spanish_regions',
            'vk_regions', 'japanese_prefixes', 'japanese_regions',
            'letters',
        ]

        for attr in required_attrs:
            self.assertTrue(hasattr(gen, attr),
                          f"Generator should have '{attr}' attribute")


class TestUSCallSignGeneration(unittest.TestCase):
    """Test US call sign generation."""

    def setUp(self):
        """Set up test generator."""
        self.gen = CallSignGenerator()

    def test_generate_us_format(self):
        """Test that US call signs match expected format."""
        for _ in range(50):
            callsign = self.gen.generate_us()

            # Should match either W1ABC or AA1ABC format
            self.assertRegex(callsign, r'^[WKNA][A-Z]?\d[A-Z]{2,3}$',
                           f"'{callsign}' should match US format")

    def test_generate_us_uniqueness(self):
        """Test that US generation produces variety."""
        callsigns = {self.gen.generate_us() for _ in range(100)}
        # Should generate at least 90 unique call signs out of 100
        self.assertGreater(len(callsigns), 90)

    def test_generate_us_region_distribution(self):
        """Test that US generation uses all regions."""
        regions_used = set()
        for _ in range(200):
            callsign = self.gen.generate_us()
            # Extract region digit
            for char in callsign:
                if char.isdigit():
                    regions_used.add(char)
                    break

        # Should use most regions (at least 8 out of 10)
        self.assertGreaterEqual(len(regions_used), 8)


class TestUKCallSignGeneration(unittest.TestCase):
    """Test UK call sign generation."""

    def setUp(self):
        """Set up test generator."""
        self.gen = CallSignGenerator()

    def test_generate_uk_format(self):
        """Test that UK call signs match expected format."""
        for _ in range(50):
            callsign = self.gen.generate_uk()
            self.assertRegex(callsign, r'^[GM]\d[A-Z]{2,4}$',
                           f"'{callsign}' should match UK format")

    def test_generate_uk_prefix_distribution(self):
        """Test that UK generation uses both G and M prefixes."""
        prefixes_used = set()
        for _ in range(100):
            callsign = self.gen.generate_uk()
            prefixes_used.add(callsign[0])

        self.assertIn('G', prefixes_used)
        self.assertIn('M', prefixes_used)


class TestEuropeanCallSignGeneration(unittest.TestCase):
    """Test European call sign generation."""

    def setUp(self):
        """Set up test generator."""
        self.gen = CallSignGenerator()

    def test_generate_german_format(self):
        """Test German call sign format."""
        for _ in range(30):
            callsign = self.gen.generate_german()
            self.assertRegex(callsign, r'^D[A-L]\d[A-Z]{2,3}$',
                           f"'{callsign}' should match German format")

    def test_generate_french_format(self):
        """Test French call sign format."""
        for _ in range(30):
            callsign = self.gen.generate_french()
            self.assertRegex(callsign, r'^F\d[A-Z]{2,3}$',
                           f"'{callsign}' should match French format")

    def test_generate_italian_format(self):
        """Test Italian call sign format."""
        for _ in range(30):
            callsign = self.gen.generate_italian()
            self.assertRegex(callsign, r'^I\d[A-Z]{2,4}$',
                           f"'{callsign}' should match Italian format")

    def test_generate_belgian_format(self):
        """Test Belgian call sign format."""
        for _ in range(30):
            callsign = self.gen.generate_belgian()
            self.assertRegex(callsign, r'^ON\d[A-Z]{2,3}$',
                           f"'{callsign}' should match Belgian format")

    def test_generate_dutch_format(self):
        """Test Dutch call sign format."""
        for _ in range(30):
            callsign = self.gen.generate_dutch()
            self.assertRegex(callsign, r'^P[ADE]\d[A-Z]{2,3}$',
                           f"'{callsign}' should match Dutch format")

    def test_generate_spanish_format(self):
        """Test Spanish call sign format."""
        for _ in range(30):
            callsign = self.gen.generate_spanish()
            self.assertRegex(callsign, r'^E[A-H]\d[A-Z]{2,3}$',
                           f"'{callsign}' should match Spanish format")


class TestAsiaPacificCallSignGeneration(unittest.TestCase):
    """Test Asia/Pacific call sign generation."""

    def setUp(self):
        """Set up test generator."""
        self.gen = CallSignGenerator()

    def test_generate_australian_format(self):
        """Test Australian call sign format."""
        for _ in range(30):
            callsign = self.gen.generate_australian()
            self.assertRegex(callsign, r'^VK[1-9][A-Z]{2,3}$',
                           f"'{callsign}' should match Australian format")

    def test_generate_japanese_format(self):
        """Test Japanese call sign format."""
        for _ in range(30):
            callsign = self.gen.generate_japanese()
            self.assertRegex(callsign, r'^J[A-S]\d[A-Z]{2,3}$',
                           f"'{callsign}' should match Japanese format")


class TestGenerateMethod(unittest.TestCase):
    """Test the main generate() method."""

    def setUp(self):
        """Set up test generator."""
        self.gen = CallSignGenerator()

    def test_generate_specific_region(self):
        """Test generating for specific regions."""
        regions = ['us', 'uk', 'germany', 'france', 'italy', 'belgium',
                  'netherlands', 'spain', 'australia', 'japan']

        for region in regions:
            callsign = self.gen.generate(region)
            self.assertIsInstance(callsign, str)
            self.assertGreater(len(callsign), 3)
            self.assertTrue(self.gen.validate_callsign(callsign),
                          f"Generated call sign '{callsign}' for {region} should be valid")

    def test_generate_random_region(self):
        """Test random region generation."""
        callsigns = [self.gen.generate() for _ in range(50)]

        for callsign in callsigns:
            self.assertIsInstance(callsign, str)
            self.assertTrue(self.gen.validate_callsign(callsign),
                          f"Generated call sign '{callsign}' should be valid")

    def test_generate_invalid_region(self):
        """Test that invalid region raises ValueError."""
        with self.assertRaises(ValueError):
            self.gen.generate('invalid_region')

    def test_generate_region_variety(self):
        """Test that random generation produces variety of regions."""
        # Generate many call signs and check we get different prefixes
        callsigns = [self.gen.generate() for _ in range(100)]
        prefixes = {cs[:2] if len(cs) > 4 else cs[:1] for cs in callsigns}

        # Should have variety of prefixes (at least 5 different ones)
        self.assertGreaterEqual(len(prefixes), 5)


class TestValidateCallsign(unittest.TestCase):
    """Test call sign validation."""

    def setUp(self):
        """Set up test generator."""
        self.gen = CallSignGenerator()

    def test_validate_valid_callsigns(self):
        """Test validation of valid call signs."""
        valid_callsigns = [
            'W1ABC', 'K6XY', 'N2MH', 'AA1AA', 'KC1XYZ',
            'G3YWX', 'M0ABC', 'DL1ABC', 'F1XYZ', 'I2ABC',
            'ON4XY', 'PA3ABC', 'EA1XYZ', 'VK2ABC', 'JA1XYZ',
        ]

        for callsign in valid_callsigns:
            self.assertTrue(self.gen.validate_callsign(callsign),
                          f"'{callsign}' should be valid")

    def test_validate_invalid_callsigns(self):
        """Test validation rejects invalid call signs."""
        invalid_callsigns = [
            '',                  # Empty
            'ABC',               # No digit
            '123',               # No letters
            'W1',                # Too short
            'W1ABCDEFG',         # Too long
            'W-1ABC',            # Invalid character
            'W 1ABC',            # Space
            '1WABC',             # Digit first
            None,                # None type
            123,                 # Wrong type
        ]

        for callsign in invalid_callsigns:
            self.assertFalse(self.gen.validate_callsign(callsign),
                           f"'{callsign}' should be invalid")

    def test_validate_accepts_lowercase(self):
        """Test that validation accepts lowercase (converts to uppercase)."""
        # Lowercase should be accepted and validated after conversion
        self.assertTrue(self.gen.validate_callsign('w1abc'),
                       'Lowercase call signs should be accepted and converted')

    def test_validate_generated_callsigns(self):
        """Test that all generated call signs pass validation."""
        for _ in range(100):
            callsign = self.gen.generate()
            self.assertTrue(self.gen.validate_callsign(callsign),
                          f"Generated '{callsign}' should be valid")


class TestCallSignFormats(unittest.TestCase):
    """Test that call signs follow realistic patterns."""

    def setUp(self):
        """Set up test generator."""
        self.gen = CallSignGenerator()

    def test_callsign_length(self):
        """Test that generated call signs have realistic lengths."""
        for _ in range(100):
            callsign = self.gen.generate()
            self.assertGreaterEqual(len(callsign), 4,
                                   f"'{callsign}' too short")
            self.assertLessEqual(len(callsign), 8,
                                f"'{callsign}' too long")

    def test_callsign_has_digit(self):
        """Test that all call signs contain at least one digit."""
        for _ in range(100):
            callsign = self.gen.generate()
            self.assertTrue(any(c.isdigit() for c in callsign),
                          f"'{callsign}' should contain a digit")

    def test_callsign_uppercase(self):
        """Test that all call signs are uppercase."""
        for _ in range(100):
            callsign = self.gen.generate()
            self.assertEqual(callsign, callsign.upper(),
                           f"'{callsign}' should be uppercase")

    def test_callsign_alphanumeric(self):
        """Test that call signs only contain alphanumeric characters."""
        for _ in range(100):
            callsign = self.gen.generate()
            self.assertTrue(callsign.isalnum(),
                          f"'{callsign}' should be alphanumeric only")


class TestCallSignDistribution(unittest.TestCase):
    """Test statistical distribution of generated call signs."""

    def setUp(self):
        """Set up test generator."""
        self.gen = CallSignGenerator()

    def test_region_weighting(self):
        """Test that region distribution follows weights."""
        # Generate many call signs and count by region
        region_counts = {}

        for _ in range(1000):
            callsign = self.gen.generate()

            # Determine region from prefix
            if callsign[0] in ['W', 'K', 'N'] or callsign[:2] in ['AA', 'KA', 'NA', 'WA']:
                region = 'us'
            elif callsign[0] in ['G', 'M']:
                region = 'uk'
            elif callsign[0] == 'D':
                region = 'germany'
            elif callsign[0] == 'F':
                region = 'france'
            elif callsign[0] == 'I':
                region = 'italy'
            elif callsign[:2] == 'ON':
                region = 'belgium'
            elif callsign[0] == 'P':
                region = 'netherlands'
            elif callsign[0] == 'E':
                region = 'spain'
            elif callsign[:2] == 'VK':
                region = 'australia'
            elif callsign[0] == 'J':
                region = 'japan'
            else:
                region = 'unknown'

            region_counts[region] = region_counts.get(region, 0) + 1

        # US should be most common (weight 30)
        self.assertGreater(region_counts.get('us', 0), 200,
                          "US should be well-represented")

        # UK should be second (weight 20)
        self.assertGreater(region_counts.get('uk', 0), 100,
                          "UK should be well-represented")


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
