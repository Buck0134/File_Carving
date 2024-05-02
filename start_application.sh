#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "myenv" ]; then
    # Create a virtual environment if it doesn't exist
    python3 -m venv myenv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source myenv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Start the application
python3 server/app.py
