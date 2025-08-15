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
        
        # Use subprocess to run the GUI
        result = subprocess.run([sys.executable, "morse_gui.py"], 
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