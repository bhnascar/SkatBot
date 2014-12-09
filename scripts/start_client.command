#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR && cd ..
# CHANGE THIS IP ADDRESS WHEN YOU PLAY
python3 skat_client.py 10.31.240.18 50007
read
