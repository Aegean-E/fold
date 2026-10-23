@echo off
setlocal EnableExtensions
title Fold
cd /d "%~dp0"

set "PYTHON_CMD=python"
where py >nul 2>&1
if not errorlevel 1 (
    py -3 -c "import sys" >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=py -3"
)

%PYTHON_CMD% run.py --open %*
if errorlevel 1 (
    echo.
    echo Fold stopped with an error. The message above says why.
    pause
)
