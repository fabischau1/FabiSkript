@echo off
:loop
color 0a
echo this will encrypt a file
set /p input="Your File Name: "
python encrypt.py %input%
goto loop