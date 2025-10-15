@echo off
REM Simple wrapper to run the PowerShell helper for Windows
powershell -ExecutionPolicy Bypass -File "%~dp0run_site.ps1" %*
