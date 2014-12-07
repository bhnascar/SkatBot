@echo off

REM Switch to the directory of the currently executing bat file
cd %~dp0

REM Switch up to the project directory
cd ..

REM Invoke Skat script
REM "-d" flag for debug (write to debug.txt instead of a log file)
REM "-b 2" flag for two bots
REM "-sa Matlab/PythonInterface/PredictSuitSoftmax.m" flag to specify suit prediction algorithm (script)
REM "-ra Matlab/PythonInterface/PredictRankSoftmax.m" flag to specify rank prediction algorithm (script)
python skat_server.py -d -b 2 -sa Matlab/PythonInterface/PredictSuitSVM.m -ra Matlab/PythonInterface/PredictRankSVM.m %*

REM Keep cmd window open after script finishes
pause
