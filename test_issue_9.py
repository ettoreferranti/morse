#!/usr/bin/env python3
"""
Test suite for Issue #9: Abbreviation Glossary Dialog

Tests the abbreviation glossary functionality including:
- Data integrity (all abbreviations present)
- Categorization
- Search filtering
- Category filtering
- UI component creation
"""

import unittest
from qso_data import ABBREVIATIONS, ABBREVIATION_CATEGORIES


class TestAbbreviationData(unittest.TestCase):
    """Test abbreviation data structure"""

    def test_abbreviations_exist(self):
        """Test that abbreviations dictionary exists and is populated"""
        self.assertIsInstance(ABBREVIATIONS, dict)
        self.assertGreater(len(ABBREVIATIONS), 0)
        self.assertEqual(len(ABBREVIATIONS), 62, "Expected 62 abbreviations")

    def test_categories_exist(self):
        """Test that categories dictionary exists"""
        self.assertIsInstance(ABBREVIATION_CATEGORIES, dict)
        self.assertGreater(len(ABBREVIATION_CATEGORIES), 0)
        self.assertEqual(len(ABBREVIATION_CATEGORIES), 7, "Expected 7 categories")

    def test_category_names(self):
        """Test expected category names"""
        expected_categories = [
            'greetings',
            'friendly',
            'common_phrases',
            'technical',
            'q_codes',
            'prosigns',
            'signal_quality'
        ]
        self.assertEqual(
            set(ABBREVIATION_CATEGORIES.keys()),
            set(expected_categories)
        )

    def test_abbreviations_have_meanings(self):
        """Test all abbreviations have non-empty meanings"""
        for abbr, meaning in ABBREVIATIONS.items():
            self.assertIsInstance(abbr, str)
            self.assertIsInstance(meaning, str)
            self.assertTrue(len(abbr) > 0)
            self.assertTrue(len(meaning) > 0)

    def test_categories_have_abbreviations(self):
        """Test all categories contain abbreviations"""
        for category, abbrs in ABBREVIATION_CATEGORIES.items():
            self.assertIsInstance(abbrs, list)
            self.assertGreater(len(abbrs), 0, f"Category {category} is empty")

    def test_category_abbreviations_valid(self):
        """Test all categorized abbreviations exist in main dict"""
        for category, abbrs in ABBREVIATION_CATEGORIES.items():
            for abbr in abbrs:
                self.assertIn(
                    abbr,
                    ABBREVIATIONS,
                    f"Abbreviation {abbr} in category {category} not in ABBREVIATIONS"
                )


class TestAbbreviationCategorization(unittest.TestCase):
    """Test abbreviation categorization logic"""

    def get_category(self, abbr):
        """Helper to find category for abbreviation"""
        for category, abbrs in ABBREVIATION_CATEGORIES.items():
            if abbr in abbrs:
                return category
        return "Other"

    def test_common_abbreviations_categorized(self):
        """Test that common abbreviations have categories"""
        # Known abbreviations from each category
        test_cases = {
            'GM': 'greetings',
            'GE': 'greetings',
            'OM': 'friendly',
            'YL': 'friendly',
            'TNX': 'common_phrases',
            'QSO': 'q_codes',
            'QTH': 'q_codes',
            'AR': 'prosigns',
            'SK': 'prosigns',
        }

        for abbr, expected_category in test_cases.items():
            category = self.get_category(abbr)
            self.assertEqual(
                category,
                expected_category,
                f"Abbreviation {abbr} should be in {expected_category}, got {category}"
            )

    def test_no_duplicate_categorization(self):
        """Test that no abbreviation appears in multiple categories"""
        all_categorized = []
        for abbrs in ABBREVIATION_CATEGORIES.values():
            all_categorized.extend(abbrs)

        # Check for duplicates
        self.assertEqual(
            len(all_categorized),
            len(set(all_categorized)),
            "Some abbreviations appear in multiple categories"
        )

    def test_categorization_coverage(self):
        """Test what percentage of abbreviations are categorized"""
        categorized = set()
        for abbrs in ABBREVIATION_CATEGORIES.values():
            categorized.update(abbrs)

        coverage = len(categorized) / len(ABBREVIATIONS) * 100
        print(f"\nCategorization coverage: {coverage:.1f}%")
        print(f"Categorized: {len(categorized)}/{len(ABBREVIATIONS)}")

        # Should have reasonable coverage (at least 70%)
        self.assertGreaterEqual(
            coverage,
            70.0,
            "Less than 70% of abbreviations are categorized"
        )


class TestSearchFiltering(unittest.TestCase):
    """Test search and filter logic"""

    def filter_abbreviations(self, search_text="", category="All"):
        """Simulate filtering logic from the dialog"""
        def get_category(abbr):
            for cat, abbrs in ABBREVIATION_CATEGORIES.items():
                if abbr in abbrs:
                    return cat
            return "Other"

        results = []
        search_upper = search_text.upper()

        for abbr, meaning in ABBREVIATIONS.items():
            cat = get_category(abbr)

            # Category filter
            if category != "All" and cat != category:
                continue

            # Search filter
            if search_upper:
                if search_upper not in abbr.upper() and search_upper not in meaning.upper():
                    continue

            results.append((abbr, meaning, cat))

        return results

    def test_no_filters_returns_all(self):
        """Test that no filters returns all abbreviations"""
        results = self.filter_abbreviations()
        self.assertEqual(len(results), len(ABBREVIATIONS))

    def test_search_by_abbreviation(self):
        """Test searching by abbreviation text"""
        results = self.filter_abbreviations(search_text="QSO")
        self.assertGreater(len(results), 0)
        # QSO should be in results
        abbrs = [r[0] for r in results]
        self.assertIn("QSO", abbrs)

    def test_search_by_meaning(self):
        """Test searching by meaning text"""
        results = self.filter_abbreviations(search_text="signal")
        self.assertGreater(len(results), 0)
        # Should find signal-related abbreviations
        for abbr, meaning, _ in results:
            self.assertTrue(
                "signal" in meaning.lower() or "signal" in abbr.lower(),
                f"Result {abbr}: {meaning} doesn't contain 'signal'"
            )

    def test_filter_by_category(self):
        """Test filtering by category"""
        results = self.filter_abbreviations(category="greetings")
        self.assertGreater(len(results), 0)
        # All results should be in greetings category
        for abbr, meaning, cat in results:
            self.assertEqual(cat, "greetings")

    def test_combined_filters(self):
        """Test combining search and category filters"""
        # Search for "good" in q_codes category
        results = self.filter_abbreviations(search_text="good", category="q_codes")
        # Should find QSL (I acknowledge receipt - "good copy")
        # Results should all be q_codes
        for abbr, meaning, cat in results:
            self.assertEqual(cat, "q_codes")

    def test_case_insensitive_search(self):
        """Test that search is case-insensitive"""
        results_lower = self.filter_abbreviations(search_text="qso")
        results_upper = self.filter_abbreviations(search_text="QSO")
        results_mixed = self.filter_abbreviations(search_text="QsO")

        self.assertEqual(len(results_lower), len(results_upper))
        self.assertEqual(len(results_lower), len(results_mixed))

    def test_empty_search_returns_all(self):
        """Test that empty search returns all results"""
        results = self.filter_abbreviations(search_text="")
        self.assertEqual(len(results), len(ABBREVIATIONS))


def _can_import_gui():
    """Check if GUI can be imported (has pyaudio)"""
    try:
        import morse_gui
        return True
    except ImportError:
        return False


class TestGlossaryIntegration(unittest.TestCase):
    """Test integration with morse_gui.py"""

    def test_imports_available(self):
        """Test that required imports work"""
        try:
            from qso_data import ABBREVIATIONS, ABBREVIATION_CATEGORIES
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import: {e}")

    @unittest.skipIf(not _can_import_gui(), "GUI dependencies not available")
    def test_gui_module_loads(self):
        """Test that morse_gui module can be imported"""
        import morse_gui
        self.assertTrue(hasattr(morse_gui, 'MorseCodeGUI'))

    @unittest.skipIf(not _can_import_gui(), "GUI dependencies not available")
    def test_glossary_method_exists(self):
        """Test that show_abbreviation_glossary method exists"""
        import morse_gui
        # Check if method exists (without instantiating GUI)
        self.assertTrue(
            hasattr(morse_gui.MorseCodeGUI, 'show_abbreviation_glossary'),
            "show_abbreviation_glossary method not found in MorseCodeGUI"
        )


def run_tests():
    """Run all tests and print summary"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAbbreviationData))
    suite.addTests(loader.loadTestsFromTestCase(TestAbbreviationCategorization))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchFiltering))
    suite.addTests(loader.loadTestsFromTestCase(TestGlossaryIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY - Issue #9: Abbreviation Glossary Dialog")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✓ ALL TESTS PASSED")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    exit(run_tests())
