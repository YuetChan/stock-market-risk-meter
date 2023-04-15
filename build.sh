#!/bin/sh
current_dir=$(dirname "$0")

cd $current_dir

PYTHON_FILE="./build.py"

# Run the Python file
python3 $PYTHON_FILE