@echo off
echo ================================================
echo Building AutoResponder1000 Executable
echo ================================================
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Install PyInstaller if not already installed
echo Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building executable...
pyinstaller --clean AutoResponder1000.spec

if errorlevel 1 (
    echo.
    echo ================================================
    echo BUILD FAILED!
    echo ================================================
    pause
    exit /b 1
)

echo.
echo ================================================
echo BUILD SUCCESSFUL!
echo ================================================
echo.
echo The executable is located at:
echo   dist\AutoResponder1000.exe
echo.
echo You can distribute this .exe file along with responses.template.json
echo.
pause
