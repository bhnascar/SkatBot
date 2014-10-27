#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
python3 skat_client.py 127.0.0.1 50007
$SHELL
