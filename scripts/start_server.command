#!/bin/sh

# Switch to project directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR && cd ..

# Invoke Skat script
# "-d" flag for debug (write to debug.txt instead of a log file)
# "-l" flag for log file folder
# "-b 2" flag for two bots
# "-sa Matlab/PythonInterface/PredictSuitSoftmax.m" flag to specify suit prediction algorithm (script)
# "-ra Matlab/PythonInterface/PredictRankSoftmax.m" flag to specify rank prediction algorithm (script)
python3 skat_server.py -d -b 2 -sa Matlab/PythonInterface/PredictSuitSoftmax.m -ra Matlab/PythonInterface/PredictRankSoftmax.m

# Keep terminal emulator open
read
