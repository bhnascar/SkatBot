#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR && cd ..
python3 skat_server.py -d -b 2 -sa Matlab/PythonInterface/PredictSuitSoftmax.m -ra Matlab/PythonInterface/PredictRankSoftmax.m
read
