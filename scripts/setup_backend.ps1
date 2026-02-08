param(
  [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv")) {
  if (Get-Command py -ErrorAction SilentlyContinue) {
    py -3 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Failed to create virtual environment with py." }
  } elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Failed to create virtual environment with python." }
  } else {
    throw "Python not found. Install Python 3.10+ first."
  }
}

$PythonExe = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
  throw "Virtual environment creation failed: $PythonExe not found."
}

if (-not $SkipInstall) {
  & $PythonExe -m pip install --upgrade pip
  if ($LASTEXITCODE -ne 0) { throw "Failed to upgrade pip." }
  & $PythonExe -m pip install -r .\backend\requirements.txt
  if ($LASTEXITCODE -ne 0) { throw "Failed to install backend requirements." }
}

if (-not (Test-Path ".\backend\.env")) {
  Copy-Item .\backend\.env.example .\backend\.env
}

Write-Host "Backend setup complete."
