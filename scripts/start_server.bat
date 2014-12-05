@echo off

REM Switch to the directory of the currently executing bat file
cd %~dp0

REM Switch up to the project directory
cd ..

REM Invoke Skat script
python skat_server.py d b 2 %*

REM Keep cmd window open after script finishes
pause
