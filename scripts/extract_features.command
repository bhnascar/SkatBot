#!/bin/sh

# Switch to project directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR && cd ..

# Run feature extraction script
python3 feature_extractor.py
echo "Done. Press any key to continue"

# Keep terminal emulator open
read
