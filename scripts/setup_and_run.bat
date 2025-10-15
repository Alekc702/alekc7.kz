@echo off
REM Wrapper to run PowerShell setup script
set SCRIPT_DIR=%~dp0
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%setup_and_run.ps1" %*
