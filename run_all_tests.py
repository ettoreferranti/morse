#!/usr/bin/env python3
"""
Comprehensive Test Runner for ALL Morse Code Tests

Runs all test files and generates unified reports:
- HTML test report with all results
- Code coverage report
- Terminal summary

Usage:
    python run_all_tests.py              # Run all tests with reports
    python run_all_tests.py --quick      # Run only unit tests (skip GUI)
    python run_all_tests.py --unit       # Run only unit tests  
    python run_all_tests.py --gui        # Run only GUI tests
"""

import sys
import os
import subprocess
from pathlib import Path
import argparse


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def discover_test_files():
    """Find all test files in the project"""
    test_files = list(Path(".").glob("test_*.py"))
    return [str(f) for f in test_files]


def run_all_tests(quick=False, unit_only=False, gui_only=False):
    """Run all tests with comprehensive reporting"""
    
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Find the Python executable (prefer venv)
    venv_python = Path("venv/bin/python")
    python = str(venv_python) if venv_python.exists() else sys.executable
    
    pytest = f"{python} -m pytest"
    
    # Determine which tests to run
    if unit_only:
        print_header("Running Unit Tests Only")
        test_pattern = "test_qso_practice.py"
    elif gui_only:
        print_header("Running GUI Tests Only")
        test_pattern = "test_gui_qso_practice.py"
    elif quick:
        print_header("Running Quick Tests (Unit Tests Only)")
        test_pattern = "test_qso_practice.py"
    else:
        print_header("Running ALL Tests (Unit + GUI + Others)")
        # Discover all test files
        test_files = discover_test_files()
        print(f"\nFound {len(test_files)} test files:")
        for f in sorted(test_files):
            print(f"  • {f}")
        print()
        test_pattern = "test_*.py"
    
    # Build command based on options
    if quick or unit_only:
        cmd = f"{pytest} {test_pattern} -v --tb=short"
    else:
        # Full test run with HTML report and coverage
        cmd = (
            f"{pytest} {test_pattern} "
            f"--html=test_report_all.html --self-contained-html "
            f"--cov=. --cov-report=term-missing --cov-report=html "
            f"-v --tb=short --timeout=30"
        )
    
    print(f"Command: {cmd}\n")
    
    # Run tests
    result = subprocess.run(cmd, shell=True)
    
    # Print results
    print_header("Test Results Summary")
    
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED!")
        print(f"Exit code: {result.returncode}")
    
    # Show where reports are located
    if not (quick or unit_only or gui_only):
        print("\n📊 Reports Generated:")
        
        if Path("test_report_all.html").exists():
            print(f"  • Unified HTML Report: {Path('test_report_all.html').absolute()}")
        
        if Path("htmlcov/index.html").exists():
            print(f"  • Coverage Report:     {Path('htmlcov/index.html').absolute()}")
        
        print("\n💡 Open these files in your browser to view detailed results!")
        print("   Example: open test_report_all.html")
        
        # Show test count summary
        print("\n📈 Test Files:")
        test_files = discover_test_files()
        for f in sorted(test_files):
            print(f"  • {f}")
    
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run all Morse Code application tests with unified reporting"
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run unit tests only without coverage or HTML reports'
    )
    parser.add_argument(
        '--unit',
        action='store_true',
        help='Run only unit tests (test_qso_practice.py)'
    )
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Run only GUI tests (test_gui_qso_practice.py)'
    )
    
    args = parser.parse_args()
    
    exit_code = run_all_tests(
        quick=args.quick,
        unit_only=args.unit,
        gui_only=args.gui
    )
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
