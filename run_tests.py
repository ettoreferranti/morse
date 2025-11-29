#!/usr/bin/env python3
"""
Comprehensive Test Runner for Morse Code Application

Runs all tests and generates:
- HTML test report with pass/fail visualization
- Code coverage report
- Terminal summary with colored output

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --quick      # Skip coverage and HTML
    python run_tests.py --coverage   # Run with coverage only
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


def run_tests(quick=False, coverage_only=False):
    """Run the test suite with various reporting options"""
    
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Find the Python executable (prefer venv)
    venv_python = Path("venv/bin/python")
    python = str(venv_python) if venv_python.exists() else sys.executable
    
    pytest = f"{python} -m pytest"
    
    if quick:
        print_header("Running Quick Tests (No Coverage/HTML)")
        cmd = f"{pytest} test_qso_practice.py -v --tb=short"
        
    elif coverage_only:
        print_header("Running Tests with Coverage Report")
        cmd = f"{pytest} test_qso_practice.py --cov=. --cov-report=term-missing --cov-report=html -v"
        
    else:
        print_header("Running Comprehensive Test Suite")
        # Full test run with HTML report and coverage
        cmd = (
            f"{pytest} test_qso_practice.py "
            f"--html=test_report.html --self-contained-html "
            f"--cov=. --cov-report=term-missing --cov-report=html "
            f"-v --tb=short"
        )
    
    print(f"\nCommand: {cmd}\n")
    
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
    if not quick:
        print("\n📊 Reports Generated:")
        
        if Path("test_report.html").exists():
            print(f"  • HTML Test Report: {Path('test_report.html').absolute()}")
        
        if Path("htmlcov/index.html").exists():
            print(f"  • Coverage Report:  {Path('htmlcov/index.html').absolute()}")
        
        print("\n💡 Open these files in your browser to view detailed results!")
        print("   Example: open test_report.html")
    
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run Morse Code application tests with reporting"
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run tests quickly without coverage or HTML reports'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Run with coverage report only (no HTML test report)'
    )
    
    args = parser.parse_args()
    
    exit_code = run_tests(quick=args.quick, coverage_only=args.coverage)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
