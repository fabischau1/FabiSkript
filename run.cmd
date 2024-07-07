@echo off
:loop
color 0a
set /p input="Your Skript Name: "
python fs.py %input%
goto loop