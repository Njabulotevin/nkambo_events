#!/bin/bash

# Check if src folder exists, if not create one
if [ ! -d "src" ]; then
    mkdir src
fi

# Check if the first argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory_name>"
    exit 1
fi

# Create directory based on the first argument inside src folder
dir_name="src/$1"
if [ ! -d "$dir_name" ]; then
    mkdir "$dir_name"
fi

# Change directory to the newly created directory
cd "$dir_name"

# Create .py files
touch "${1}Controller.py"
touch "${1}Model.py"
touch "${1}DAO.py"
touch "${1}Service.py"

echo "Files created successfully in $dir_name directory."

