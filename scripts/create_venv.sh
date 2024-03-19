#!/bin/bash

# Name of the virtual environment (you can change this as needed)
VENV_NAME="venv"

# Check if the virtual environment already exists
if [ -d "$VENV_NAME" ]; then
    echo "Virtual environment '$VENV_NAME' already exists."
    exit 1
fi

# Create the virtual environment
python3 -m venv "$VENV_NAME"

# Print instructions for activating and deactivating the virtual environment
echo "Virtual environment '$VENV_NAME' created."
echo "To activate the virtual environment, run: source ./$VENV_NAME/bin/activate (Linux/Mac)"
echo "To activate the virtual environment, run: .\\$VENV_NAME\Scripts\Activate.ps1 (WINDOWS)"
echo "To install packages, run: pip install -r requirements.txt"
echo "To deactivate the virtual environment, run: deactivate"
