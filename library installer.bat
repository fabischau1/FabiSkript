@echo off
color 0a

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo Python is installed.
)

REM Check and install cryptography
python -c "import cryptography" > nul 2>&1
if errorlevel 1 (
    echo Installing cryptography...
    pip install cryptography
) else (
    echo cryptography is already installed.
)

python -c "from plyer import notification" > nul 2>&1
if errorlevel 1 (
    echo Installing plyer...
    pip install plyer
) else (
    echo plyer is already installed.
)

echo Installation complete.
pause
