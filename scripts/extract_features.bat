@echo off

REM Switch to the directory of the currently executing bat file
cd %~dp0

REM Switch up to the project directory
cd ..

REM Invoke feature extraction script
python feature_extractor.py

REM Keep cmd window open after script finishes
pause
