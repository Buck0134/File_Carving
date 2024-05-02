@echo off

REM Check if the virtual environment directory exists
IF NOT EXIST "myenv" (
    REM Create a virtual environment if it doesn't exist
    python -m venv myenv
    echo Virtual environment created.
) ELSE (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
myenv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Start the application
python server\app.py
