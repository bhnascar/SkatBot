#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR && cd ..
python3 feature_extractor.py
echo "Done. Press any key to continue"
read
