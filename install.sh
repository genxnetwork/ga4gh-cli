#!/bin/bash

# Build and package the source distribution and binary wheel
python3 setup.py sdist bdist_wheel

# Install the package and its dependencies using pip and the requirements file
pip install dist/ga4gh-cli-*.tar.gz -r requirements.txt

# Check if the installation was successful
ga4gh-cli --version