@echo off

REM Switch to the directory of the currently executing bat file
cd %~dp0

REM Invoke Skat script
python skat_client.py 128.12.20.104 50007

REM Keep cmd window open after script finishes
pause
