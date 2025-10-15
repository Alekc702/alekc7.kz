<#
Setup script for Windows PowerShell to prepare the project and run the dev server.
Usage examples:
  .\scripts\setup_and_run.ps1          # run with defaults
  .\scripts\setup_and_run.ps1 -NoInstallDeps -NoCollectStatic -RunServerOnly
#>

[CmdletBinding()]
param(
    [switch]$NoCreateVenv,
    [switch]$NoInstallDeps,
    [switch]$NoCollectStatic,
    [switch]$RunServerOnly,
    [int]$Port = 8000
)

Set-StrictMode -Version Latest

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location $root

Write-Host "Working directory: $root"

# 1) Create venv
if (-not $NoCreateVenv) {
    if (-not (Test-Path "$root\venv")) {
        Write-Host "Creating virtualenv..."
        python -m venv "$root\venv"
    } else {
        Write-Host "Virtualenv exists: $root\venv"
    }
}

# Helper paths
$venvPython = "$root\venv\Scripts\python.exe"
$venvPip = "$root\venv\Scripts\pip.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Warning: venv python not found at $venvPython. Ensure 'python' is on PATH or run script with CreateVenv enabled." -ForegroundColor Yellow
}

if (-not $NoInstallDeps) {
    Write-Host "Upgrading pip, setuptools, wheel..."
    & $venvPip install -U pip setuptools wheel
    Write-Host "Installing requirements.txt..."
    & $venvPip install -r requirements.txt
}

Write-Host "Ensuring storage directories (STATIC_ROOT and MEDIA_ROOT)..."
& $venvPython manage.py ensure_storage

if (-not $RunServerOnly) {
    Write-Host "Applying migrations..."
    & $venvPython manage.py migrate

    if (-not $NoCollectStatic) {
        Write-Host "Collecting static files..."
        & $venvPython manage.py collectstatic --noinput
    }
}

if ($RunServerOnly -or -not $NoCollectStatic) {
    Write-Host "Starting development server on 0.0.0.0:$Port ..."
    & $venvPython manage.py runserver 0.0.0.0:$Port
}

Pop-Location
