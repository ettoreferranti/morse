# Testing Guide

## Quick Start

Run all tests with visual HTML reports:

```bash
python run_tests.py
```

This will:
- ✅ Run all 16 tests
- 📊 Generate HTML test report with pass/fail visualization
- 📈 Generate code coverage report  
- 🌐 Auto-open both reports in your browser

## Test Runner Options

### Full Report (Default)
```bash
python run_tests.py
```
Generates HTML test report + coverage report

### Quick Run (No Reports)
```bash
python run_tests.py --quick
```
Fast execution, terminal output only

### Coverage Only
```bash
python run_tests.py --coverage
```
Generates coverage report but not HTML test report

## Visual Reports

### 1. HTML Test Report (`test_report.html`)

**Features:**
- ✅ Green checkmarks for passing tests
- ❌ Red X for failing tests
- ⏱️ Execution time for each test
- 📝 Test descriptions and error details
- 📊 Summary statistics

**To view:**
```bash
open test_report.html
```

### 2. Coverage Report (`htmlcov/index.html`)

**Features:**
- 📈 Overall code coverage percentage
- 📂 File-by-file coverage breakdown
- 🔴 Red highlighting for uncovered lines
- 🟢 Green highlighting for covered lines
- 📊 Coverage graphs and charts

**To view:**
```bash
open htmlcov/index.html
```

## Current Test Suite

### Core Tests (16 total)

**QSO Practice Session** (6 tests)
- ✅ Session initialization
- ✅ Playback state transitions
- ✅ Pause/Resume functionality
- ✅ Stop functionality
- ✅ Replay functionality
- ✅ Playback completion

**Submit During Playback** (2 tests) 🔥 CRITICAL
- ✅ Submit while playing (bug fix)
- ✅ Submit while paused (bug fix)

**State Callbacks** (2 tests)
- ✅ State change callbacks fire
- ✅ Playback complete callback fires

**QSO Generation** (2 tests)
- ✅ Generate minimal QSO
- ✅ Get morse text

**Scoring** (2 tests)
- ✅ Scorer creation
- ✅ Session scorer

**Edge Cases** (2 tests)
- ✅ Session summary
- ✅ Rapid state changes

## Test Coverage

Current coverage for QSO practice modules:
- `qso_data.py`: 76%
- `qso_practice.py`: 66%
- `test_qso_practice.py`: 97% (the test file itself!)

## Adding New Tests

1. Add tests to `test_qso_practice.py`:

```python
class TestNewFeature(unittest.TestCase):
    """Test description"""
    
    def setUp(self):
        # Setup code
        self.session = QSOPracticeSession(...)
    
    def test_specific_behavior(self):
        """Test specific aspect"""
        self.session.do_something()
        self.assertEqual(self.session.state, 'expected')
```

2. Run tests to verify:
```bash
python run_tests.py
```

3. Check the HTML report to see your new test!

## Other Test Files

The project also has these test files (not currently in test runner):
- `test_callsign_generator.py` - Callsign generation tests
- `test_glossary_dialog.py` - Glossary UI tests  
- `test_issue_9.py` - Issue #9 specific tests
- `test_qso_data.py` - QSO data generation tests
- `test_qso_generator.py` - QSO generator tests
- `test_qso_scoring.py` - Scoring system tests
- `test_qso_template.py` - Template system tests

To run all tests:
```bash
python -m pytest -v
```

## Continuous Integration

Before committing:

```bash
# Run tests
python run_tests.py

# If all pass, commit
git add .
git commit -m "Your message"
```

## Manual Test Running

### Using pytest directly:
```bash
# All tests
pytest test_qso_practice.py -v

# Specific test class
pytest test_qso_practice.py::TestSubmitDuringPlayback -v

# Single test
pytest test_qso_practice.py::TestSubmitDuringPlayback::test_submit_during_playback -v
```

### Using unittest:
```bash
# All tests
python -m unittest test_qso_practice.py -v

# Specific test class
python -m unittest test_qso_practice.TestSubmitDuringPlayback -v
```

## Interpreting Results

### Terminal Output

**Green PASSED**: Test passed ✅
```
test_submit_during_playback PASSED [ 50%]
```

**Red FAILED**: Test failed ❌
```
test_submit_during_playback FAILED [ 50%]
```

### HTML Report

- Click on any test to see details
- Failed tests show full error traceback
- Summary at top shows pass/fail counts
- Execution time shown for each test

### Coverage Report

- Green lines: Covered by tests
- Red lines: Not covered
- Yellow lines: Partially covered
- Click file names to see line-by-line coverage

## Troubleshooting

**Tests fail with import errors:**
```bash
# Make sure you're using venv Python
source venv/bin/activate
python run_tests.py
```

**HTML reports not opening:**
```bash
# Open manually
open test_report.html
open htmlcov/index.html
```

**Coverage seems low:**
- Coverage includes ALL Python files
- GUI files (`morse_gui.py`) need GUI tests (not yet implemented)
- Focus on coverage for files under test
