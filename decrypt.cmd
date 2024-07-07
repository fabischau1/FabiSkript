@echo off
:loop
color 0a
echo this will decrypt a file
set /p input="Your File Name: "
python decrypt.py %input%
goto loop