#!/bin/bash

# Define directories and files to remove
DIRECTORIES=("dist" "build")
FILES=("*.pyc")

# Remove directories
for dir in "${DIRECTORIES[@]}"; do
    if [ -d "$dir" ]; then
        echo "Removing directory: $dir"
        rm -rf "$dir"
    fi
done

# Remove files
for pattern in "${FILES[@]}"; do
    find . -type f -name "$pattern" -exec rm -f {} \;
done

# Optionally, remove additional files or directories
# Add more commands here as needed

echo "Cleanup complete."
