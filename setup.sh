#!/bin/bash

# Define the virtual environment directory name
VENV_DIR="venv"

# Step 1: Check if a virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment '$VENV_DIR' already exists."
else
    # Step 2: Create the virtual environment
    echo "Creating virtual environment '$VENV_DIR'..."
    python3 -m venv ./venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Make sure Python is installed."
        exit 1
    fi
    echo "Virtual environment created successfully."
fi

# Step 3: Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi
echo "Virtual environment activated."

# Step 4: Install dependencies from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies. Check your requirements.txt file."
        deactivate
        exit 1
    fi
    echo "Dependencies installed successfully."
else
    echo "No requirements.txt file found. Skipping dependency installation."
fi

echo "Setup completed successfully. Virtual environment is active."
