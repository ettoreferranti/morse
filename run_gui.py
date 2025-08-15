#!/usr/bin/env python3
"""
Simple launcher script for the Morse Code GUI application.

This script provides an easy way to launch the GUI version
with proper error handling and user feedback.
"""

import sys
import os

def main():
    """Launch the Morse Code GUI application"""
    try:
        # Check if we can import tkinter
        try:
            import tkinter as tk
        except ImportError:
            print("Error: tkinter is not available.")
            print("Please install tkinter or use the command-line version (python morse.py)")
            return 1
        
        # Check if we have the required modules
        try:
            from morse_gui import main as gui_main
        except ImportError as e:
            print(f"Error: Failed to import GUI module: {e}")
            print("Make sure morse_gui.py is in the same directory")
            return 1
        
        print("Starting Morse Code GUI Application...")
        print("Close the window to exit.")
        
        # Launch the GUI
        gui_main()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 0
    except Exception as e:
        print(f"Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())