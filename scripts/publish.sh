#!/bin/bash

# Ensure script is run from project root directory
if [ ! -f setup.py ]; then
    echo "Error: Script must be run from the project root directory."
    exit 1
fi

# Clean up previous build artifacts (optional)
echo "Cleaning up previous build artifacts..."
rm -rf dist build

# Create source distribution and wheel
echo "Building source distribution and wheel..."
python3 setup.py sdist bdist_wheel

# Display build artifacts (optional)
echo "Build artifacts:"
ls -l dist/

# Upload to PyPI (replace with your PyPI username)
echo "Uploading to PyPI..."
twine upload dist/* --verbose

echo "Publishing complete."
