@echo off

REM Switch to the directory of the currently executing bat file
cd %~dp0

REM Invoke Skat script
python skat_client.py 127.0.0.1 50007

REM Keep cmd window open after script finishes
pause
