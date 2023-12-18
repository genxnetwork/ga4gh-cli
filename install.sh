#!/bin/bash

python3 -m venv venv
source venv/bin/activate

# Build and package the source distribution and binary wheel
python3 setup.py sdist bdist_wheel

# Install the package using pip
pip install .

# Check if the installation was successful
ga4gh-cli --version