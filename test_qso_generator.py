"""
Unit tests for QSOGenerator class

Tests complete QSO generation integration.

Author: Generated with Claude Code
Date: 2025-11-28
Issue: #5 - QSO Feature: QSO Generator Integration
"""

import unittest
from qso_data import QSOGenerator, CallSignGenerator
import qso_data


class TestQSOGeneratorInit(unittest.TestCase):
    """Test QSOGenerator initialization."""

    def test_initialization(self):
        """Test that generator initializes correctly."""
        gen = QSOGenerator()
        self.assertIsInstance(gen, QSOGenerator)
        self.assertTrue(hasattr(gen, 'call_gen'))
        self.assertTrue(hasattr(gen, 'template_gen'))
        self.assertTrue(hasattr(gen, 'random'))

    def test_initialization_with_seed(self):
        """Test initialization with random seed stores seed."""
        gen = QSOGenerator(seed=42)

        # Should store seed
        self.assertEqual(gen.seed, 42)

        # Should be able to generate station data
        station = gen.generate_station_data()
        self.assertIsInstance(station, dict)
        self.assertIn('callsign', station)


class TestRandomSelectionMethods(unittest.TestCase):
    """Test random data selection methods."""

    def setUp(self):
        """Set up test generator."""
        self.gen = QSOGenerator()

    def test_select_random_name(self):
        """Test random name selection."""
        name = self.gen._select_random_name()
        self.assertIsInstance(name, str)
        self.assertIn(name, qso_data.COMMON_NAMES)

    def test_select_random_city(self):
        """Test random city selection."""
        city = self.gen._select_random_city()
        self.assertIsInstance(city, str)
        self.assertIn(city, qso_data.ALL_CITIES)

    def test_select_random_transceiver(self):
        """Test random transceiver selection."""
        rig = self.gen._select_random_transceiver()
        self.assertIsInstance(rig, str)
        self.assertIn(rig, qso_data.TRANSCEIVERS)

    def test_select_random_antenna(self):
        """Test random antenna selection."""
        ant = self.gen._select_random_antenna()
        self.assertIsInstance(ant, str)
        self.assertIn(ant, qso_data.ANTENNAS)

    def test_select_random_power(self):
        """Test random power selection."""
        pwr = self.gen._select_random_power()
        self.assertIsInstance(pwr, str)
        self.assertIn(pwr, qso_data.POWER_LEVELS)

    def test_select_random_weather(self):
        """Test random weather selection."""
        wx = self.gen._select_random_weather()
        self.assertIsInstance(wx, str)
        self.assertIn(wx, qso_data.WEATHER_CONDITIONS)

    def test_select_random_temperature(self):
        """Test random temperature selection."""
        temp = self.gen._select_random_temperature()
        self.assertIsInstance(temp, str)
        self.assertIn(temp, qso_data.TEMPERATURES)

    def test_select_random_rst(self):
        """Test random RST selection."""
        rst = self.gen._select_random_rst()
        self.assertIsInstance(rst, str)
        self.assertIn(rst, qso_data.RST_REPORTS)

    def test_selection_variety(self):
        """Test that selections show variety."""
        names = [self.gen._select_random_name() for _ in range(20)]
        unique_names = set(names)
        self.assertGreater(len(unique_names), 3, "Should have variety in names")


class TestStationDataGeneration(unittest.TestCase):
    """Test station data generation."""

    def setUp(self):
        """Set up test generator."""
        self.gen = QSOGenerator()

    def test_generate_station_data_structure(self):
        """Test that station data has correct structure."""
        station = self.gen.generate_station_data()

        # Check all required fields present
        required_fields = [
            'callsign', 'name', 'qth', 'rst', 'rig',
            'antenna', 'power', 'weather', 'temperature'
        ]
        for field in required_fields:
            self.assertIn(field, station)
            self.assertIsInstance(station[field], str)

    def test_generate_station_data_valid(self):
        """Test that generated station data is valid."""
        station = self.gen.generate_station_data()

        # Validate call sign
        call_gen = CallSignGenerator()
        self.assertTrue(call_gen.validate_callsign(station['callsign']))

        # Validate name
        self.assertTrue(qso_data.validate_name(station['name']))

        # Validate QTH
        self.assertTrue(qso_data.validate_qth(station['qth']))

        # Validate RST
        self.assertTrue(qso_data.validate_rst(station['rst']))

        # Validate equipment
        self.assertTrue(qso_data.validate_equipment(station['rig']))
        self.assertTrue(qso_data.validate_equipment(station['antenna']))

        # Validate power
        self.assertTrue(qso_data.validate_power(station['power']))

    def test_generate_station_with_region(self):
        """Test station generation with specific call region."""
        station_us = self.gen.generate_station_data(call_region='us')
        station_uk = self.gen.generate_station_data(call_region='uk')

        # US call signs start with W, K, N, A
        self.assertTrue(station_us['callsign'][0] in 'WKNA')

        # UK call signs start with G or M
        self.assertTrue(station_uk['callsign'][0] in 'GM')

    def test_multiple_stations_unique(self):
        """Test that multiple stations are unique."""
        stations = [self.gen.generate_station_data() for _ in range(10)]

        # Should have variety in callsigns
        callsigns = [s['callsign'] for s in stations]
        unique_callsigns = set(callsigns)
        self.assertGreater(len(unique_callsigns), 5)


class TestQSOGeneration(unittest.TestCase):
    """Test complete QSO generation."""

    def setUp(self):
        """Set up test generator."""
        self.gen = QSOGenerator()

    def test_generate_qso_structure(self):
        """Test that generated QSO has correct structure."""
        qso = self.gen.generate_qso()

        # Check all required top-level fields
        required_fields = [
            'calling_station', 'responding_station',
            'full_text', 'verbosity', 'template', 'elements'
        ]
        for field in required_fields:
            self.assertIn(field, qso)

    def test_generate_qso_stations(self):
        """Test that QSO contains valid station data."""
        qso = self.gen.generate_qso()

        # Both stations should have all fields
        for station in [qso['calling_station'], qso['responding_station']]:
            required_fields = [
                'callsign', 'name', 'qth', 'rst', 'rig',
                'antenna', 'power', 'weather', 'temperature'
            ]
            for field in required_fields:
                self.assertIn(field, station)

    def test_generate_qso_full_text(self):
        """Test that QSO full_text is generated."""
        qso = self.gen.generate_qso()

        self.assertIsInstance(qso['full_text'], str)
        self.assertGreater(len(qso['full_text']), 100)

        # Should start with CQ
        self.assertTrue(qso['full_text'].strip().startswith('CQ'))

        # Should contain call signs
        self.assertIn(qso['calling_station']['callsign'], qso['full_text'])
        self.assertIn(qso['responding_station']['callsign'], qso['full_text'])

        # Should contain names
        self.assertIn(qso['calling_station']['name'], qso['full_text'])
        self.assertIn(qso['responding_station']['name'], qso['full_text'])

    def test_generate_qso_verbosity_minimal(self):
        """Test minimal verbosity QSO generation."""
        qso = self.gen.generate_qso(verbosity='minimal')

        self.assertEqual(qso['verbosity'], 'minimal')
        self.assertIsInstance(qso['full_text'], str)

    def test_generate_qso_verbosity_medium(self):
        """Test medium verbosity QSO generation."""
        qso = self.gen.generate_qso(verbosity='medium')

        self.assertEqual(qso['verbosity'], 'medium')
        # Medium should contain equipment
        self.assertIn(qso['calling_station']['rig'], qso['full_text'])

    def test_generate_qso_verbosity_chatty(self):
        """Test chatty verbosity QSO generation."""
        qso = self.gen.generate_qso(verbosity='chatty')

        self.assertEqual(qso['verbosity'], 'chatty')
        # Chatty should contain weather
        self.assertIn(qso['calling_station']['weather'], qso['full_text'])

    def test_generate_qso_with_regions(self):
        """Test QSO generation with specific regions."""
        qso = self.gen.generate_qso(call_region1='us', call_region2='uk')

        # Verify regions
        self.assertTrue(qso['calling_station']['callsign'][0] in 'WKNA')
        self.assertTrue(qso['responding_station']['callsign'][0] in 'GM')

    def test_generate_qso_elements(self):
        """Test that QSO elements are correctly structured."""
        qso = self.gen.generate_qso()

        # Elements should have station1 and station2
        self.assertIn('station1', qso['elements'])
        self.assertIn('station2', qso['elements'])

        # Each station should have key fields
        for station_key in ['station1', 'station2']:
            station = qso['elements'][station_key]
            for field in ['callsign', 'name', 'qth', 'rst', 'rig', 'antenna', 'power']:
                self.assertIn(field, station)

    def test_generate_qso_invalid_verbosity(self):
        """Test that invalid verbosity raises error."""
        with self.assertRaises(ValueError):
            self.gen.generate_qso(verbosity='invalid')


class TestQSOExtraction(unittest.TestCase):
    """Test QSO element extraction."""

    def setUp(self):
        """Set up test generator."""
        self.gen = QSOGenerator()

    def test_extract_qso_elements(self):
        """Test extraction of QSO elements."""
        qso = self.gen.generate_qso()
        elements = self.gen.extract_qso_elements(qso)

        # Check all required element types
        required = ['callsigns', 'names', 'qths', 'rsts', 'rigs', 'antennas', 'powers']
        for elem_type in required:
            self.assertIn(elem_type, elements)
            self.assertIsInstance(elements[elem_type], list)
            self.assertEqual(len(elements[elem_type]), 2)

    def test_extract_callsigns(self):
        """Test extraction of callsigns."""
        qso = self.gen.generate_qso()
        elements = self.gen.extract_qso_elements(qso)

        self.assertEqual(elements['callsigns'][0], qso['calling_station']['callsign'])
        self.assertEqual(elements['callsigns'][1], qso['responding_station']['callsign'])

    def test_extract_names(self):
        """Test extraction of names."""
        qso = self.gen.generate_qso()
        elements = self.gen.extract_qso_elements(qso)

        self.assertEqual(elements['names'][0], qso['calling_station']['name'])
        self.assertEqual(elements['names'][1], qso['responding_station']['name'])


class TestMorseTextExtraction(unittest.TestCase):
    """Test Morse text extraction."""

    def setUp(self):
        """Set up test generator."""
        self.gen = QSOGenerator()

    def test_get_morse_text(self):
        """Test extraction of Morse-ready text."""
        qso = self.gen.generate_qso()
        morse_text = self.gen.get_morse_text(qso)

        self.assertIsInstance(morse_text, str)
        self.assertEqual(morse_text, qso['full_text'])

    def test_morse_text_format(self):
        """Test that Morse text is properly formatted."""
        qso = self.gen.generate_qso()
        morse_text = self.gen.get_morse_text(qso)

        # Should be uppercase
        self.assertEqual(morse_text, morse_text.upper())

        # Should contain typical Morse elements
        self.assertIn('CQ', morse_text)
        self.assertIn('DE', morse_text)
        self.assertIn('K', morse_text)
        self.assertIn('SK', morse_text)


class TestMultipleQSOGeneration(unittest.TestCase):
    """Test generation of multiple QSOs."""

    def setUp(self):
        """Set up test generator."""
        self.gen = QSOGenerator()

    def test_generate_multiple_qsos(self):
        """Test generation of multiple QSOs."""
        qsos = self.gen.generate_multiple_qsos(count=5)

        self.assertIsInstance(qsos, list)
        self.assertEqual(len(qsos), 5)

        # Each should be a valid QSO
        for qso in qsos:
            self.assertIn('calling_station', qso)
            self.assertIn('full_text', qso)

    def test_generate_multiple_with_verbosity(self):
        """Test multiple QSO generation with specific verbosity."""
        qsos = self.gen.generate_multiple_qsos(count=3, verbosity='chatty')

        self.assertEqual(len(qsos), 3)
        for qso in qsos:
            self.assertEqual(qso['verbosity'], 'chatty')

    def test_multiple_qsos_unique(self):
        """Test that multiple QSOs are unique."""
        qsos = self.gen.generate_multiple_qsos(count=10)

        # Should have variety in callsigns
        callsigns = [qso['calling_station']['callsign'] for qso in qsos]
        unique_callsigns = set(callsigns)
        self.assertGreater(len(unique_callsigns), 5)

        # Should have variety in full text
        texts = [qso['full_text'] for qso in qsos]
        unique_texts = set(texts)
        self.assertGreater(len(unique_texts), 5)

    def test_generate_multiple_invalid_count(self):
        """Test that invalid count raises error."""
        with self.assertRaises(ValueError):
            self.gen.generate_multiple_qsos(count=0)

        with self.assertRaises(ValueError):
            self.gen.generate_multiple_qsos(count=101)

        with self.assertRaises(ValueError):
            self.gen.generate_multiple_qsos(count='invalid')


class TestIntegration(unittest.TestCase):
    """Test integration with other components."""

    def setUp(self):
        """Set up test generator."""
        self.gen = QSOGenerator()

    def test_integration_with_callsign_generator(self):
        """Test integration with CallSignGenerator."""
        qso = self.gen.generate_qso()

        # Call signs should be valid
        call_gen = CallSignGenerator()
        self.assertTrue(call_gen.validate_callsign(qso['calling_station']['callsign']))
        self.assertTrue(call_gen.validate_callsign(qso['responding_station']['callsign']))

    def test_integration_with_template_system(self):
        """Test integration with QSOTemplate."""
        qso = self.gen.generate_qso()

        # Should have template field
        self.assertIn('template', qso)
        self.assertIsInstance(qso['template'], str)

        # Template should contain placeholders before substitution
        self.assertIn('{CALL', qso['template'])

    def test_integration_with_validation(self):
        """Test that all generated data passes validation."""
        qso = self.gen.generate_qso()

        # Validate all station data
        for station in [qso['calling_station'], qso['responding_station']]:
            self.assertTrue(qso_data.validate_name(station['name']))
            self.assertTrue(qso_data.validate_qth(station['qth']))
            self.assertTrue(qso_data.validate_rst(station['rst']))
            self.assertTrue(qso_data.validate_equipment(station['rig']))
            self.assertTrue(qso_data.validate_equipment(station['antenna']))
            self.assertTrue(qso_data.validate_power(station['power']))

    def test_end_to_end_workflow(self):
        """Test complete end-to-end QSO generation workflow."""
        # Generate QSO
        qso = self.gen.generate_qso(verbosity='medium')

        # Extract elements for scoring
        elements = self.gen.extract_qso_elements(qso)

        # Get Morse text
        morse_text = self.gen.get_morse_text(qso)

        # Verify workflow
        self.assertIsInstance(qso, dict)
        self.assertIsInstance(elements, dict)
        self.assertIsInstance(morse_text, str)

        # Verify elements match QSO
        self.assertEqual(elements['callsigns'][0], qso['calling_station']['callsign'])
        self.assertEqual(morse_text, qso['full_text'])


class TestReproducibility(unittest.TestCase):
    """Test seeding support."""

    def test_seed_stored(self):
        """Test that seed is stored for potential future use."""
        gen = QSOGenerator(seed=123)
        self.assertEqual(gen.seed, 123)

        gen_no_seed = QSOGenerator()
        self.assertIsNone(gen_no_seed.seed)

    def test_generator_produces_varied_output(self):
        """Test that generator produces variety without seed."""
        gen = QSOGenerator()

        qsos = [gen.generate_qso() for _ in range(10)]

        # Should have variety
        callsigns = [q['calling_station']['callsign'] for q in qsos]
        unique_callsigns = set(callsigns)
        self.assertGreater(len(unique_callsigns), 3)


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
