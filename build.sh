#!/bin/bash

# Clean up previous build artifacts (optional)
echo "Cleaning up previous build artifacts..."
rm -rf dist build

# Create source distribution and wheel
echo "Building source distribution and wheel..."
python3 setup.py sdist bdist_wheel

# Display build artifacts
echo "Build artifacts:"
ls -l dist/

echo "Build complete."
