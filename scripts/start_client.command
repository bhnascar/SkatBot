#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR && cd ..
# CHANGE THIS IP ADDRESS WHEN YOU PLAY
python3 skat_client.py 127.0.0.1 50007
read
