@echo off
setlocal
title BarcodeGenerator

set "PROJECT_DIR=%~dp0"

if not exist "%PROJECT_DIR%main.py" (
    echo This launcher is not in the BarcodeGenerator project folder.
    set /p "PROJECT_DIR=Enter the full path to the cloned BarcodeGenerator folder: "
)

if not exist "%PROJECT_DIR%\main.py" (
    echo Could not find main.py in "%PROJECT_DIR%".
    pause
    exit /b 1
)

where uv >nul 2>&1
if errorlevel 1 (
    echo uv is not installed or is not available on PATH.
    pause
    exit /b 1
)

pushd "%PROJECT_DIR%"
uv run --locked main.py
set "EXIT_CODE=%ERRORLEVEL%"
popd

if not "%EXIT_CODE%"=="0" pause
exit /b %EXIT_CODE%
