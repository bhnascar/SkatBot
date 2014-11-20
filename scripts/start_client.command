#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR && cd ..
# CHANGE THIS IP ADDRESS WHEN YOU PLAY
python3 skat_client.py 10.31.243.85 50007
read
