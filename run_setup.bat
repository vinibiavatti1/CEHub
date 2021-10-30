@echo off

REM Create venv
if not exist .\.venv\Scripts\python.exe (
    echo Installing environment...
    python -m venv .venv
    echo Virtual environment installed in /.venv folder
)

REM Activate
echo Activating virtual environment...
cd .\.venv\Scripts
call activate.bat
echo Environment activated

REM Updating PIP
echo Updating PIP...
python -m pip install --upgrade pip
echo PIP updated

REM Install dependencies
echo Installing project dependencies...
cd ..\..
python -m pip install -r requirements.txt
echo Dependencies installed

REM Done
echo Project setup successfully!
pause
