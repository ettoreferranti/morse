#!/bin/bash
# Morse Code GUI Launcher Script
# This script ensures the GUI runs with the correct Python environment

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$DIR"

echo "Starting Morse Code GUI Application..."
echo "Directory: $DIR"

# Try to activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Check Python version
echo "Python version: $(python3 --version)"
echo "Python path: $(which python3)"

# Try to run the GUI
echo "Launching GUI..."
python3 morse_gui.py

echo "GUI closed. Press any key to exit..."
read -n 1