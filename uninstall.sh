#!/bin/bash

# Step 1: Check if the virtual environment is active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "No virtual environment is currently active."
    echo "Please activate a virtual environment before running this script."
    exit 1
fi

# Step 2: List all installed packages and uninstall them
echo "Uninstalling all packages from the active virtual environment..."
pip freeze | xargs pip uninstall -y

# Step 3: Confirm uninstallation
echo "All packages have been uninstalled."
