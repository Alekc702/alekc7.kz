<#
Run-site helper script for Windows PowerShell

Usage examples:
  .\run_site.ps1                         # create venv if missing, install, migrate, runserver on 0.0.0.0:8000 and open browser
  .\run_site.ps1 -SkipInstall -NoBrowser -Port 8080
  .\run_site.ps1 -SkipMigrate

Options:
  -SkipInstall    : don't run pip install -r requirements.txt
  -SkipMigrate    : don't run makemigrations/migrate
  -NoBrowser      : don't open browser automatically
  -Port <int>     : port to run the dev server on (default 8000)
#>

param(
    [switch]$SkipInstall,
    [switch]$SkipMigrate,
    [switch]$NoBrowser,
    [int]$Port = 8000
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "Running run_site.ps1 (Port=$Port, SkipInstall=$SkipInstall, SkipMigrate=$SkipMigrate, NoBrowser=$NoBrowser)"

# prefer py -3.11 if available, otherwise fall back to py -3
$pyCmd = 'py -3.11'
try { & py -3.11 --version > $null 2>&1 } catch { $pyCmd = 'py -3' }

$venvPath = Join-Path $PSScriptRoot 'venv'
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at: $venvPath"
    & $pyCmd -m venv $venvPath
}

# Activate the virtualenv for this script
Write-Host "Activating virtual environment: $venvPath"
. "$venvPath\Scripts\Activate.ps1"

if (-not $SkipInstall) {
    Write-Host "Upgrading pip/setuptools/wheel and installing requirements..."
    python -m pip install --upgrade pip setuptools wheel
    $req = Join-Path $PSScriptRoot 'requirements.txt'
    if (Test-Path $req) {
        pip install -r $req
    } else {
        Write-Host "No requirements.txt found in project root. Skipping pip install."
    }
}

if (-not $SkipMigrate) {
    Write-Host "Applying migrations..."
    python manage.py makemigrations
    python manage.py migrate
}

$url = "http://127.0.0.1:$Port"
if (-not $NoBrowser) {
    Write-Host "Opening browser: $url"
    Start-Process $url
}

Write-Host "Starting Django development server on 0.0.0.0:$Port"
python manage.py runserver "0.0.0.0:$Port"
