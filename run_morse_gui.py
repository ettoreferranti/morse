#!/usr/bin/env python3
"""
Simple wrapper to launch the Morse Code GUI with better error handling
"""

import sys
import os
import subprocess

def main():
    print("=== Morse Code GUI Launcher ===")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"Working directory: {script_dir}")
    
    # Check if we have the required files
    if not os.path.exists("morse_gui.py"):
        print("ERROR: morse_gui.py not found!")
        input("Press Enter to exit...")
        return 1
    
    if not os.path.exists("morse.py"):
        print("ERROR: morse.py not found!")
        input("Press Enter to exit...")
        return 1
        
    # Try to run the GUI
    try:
        print("Launching Morse Code GUI...")
        print("Close the GUI window to return to this launcher.")
        print("")

        # Check if virtual environment exists
        venv_python = os.path.join(script_dir, "venv", "bin", "python")
        if os.path.exists(venv_python):
            print("Using virtual environment Python...")
            python_executable = venv_python
        else:
            print("Virtual environment not found, using system Python...")
            print("Note: You may need to run: python3 -m venv venv && venv/bin/pip install pyaudio numpy")
            python_executable = sys.executable

        # Use subprocess to run the GUI
        result = subprocess.run([python_executable, "morse_gui.py"],
                              cwd=script_dir,
                              capture_output=False)
        
        if result.returncode == 0:
            print("GUI closed normally.")
        else:
            print(f"GUI exited with code: {result.returncode}")
            
    except FileNotFoundError:
        print("ERROR: Python interpreter not found!")
        print("Make sure Python is installed correctly.")
    except Exception as e:
        print(f"ERROR: {e}")
    
    input("Press Enter to exit...")
    return 0

if __name__ == "__main__":
    sys.exit(main())