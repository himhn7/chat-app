param(
  [switch]$InstallDeps
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv")) {
  & .\scripts\setup_backend.ps1
}

$PythonExe = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
  throw "Python executable not found in .venv."
}

if ($InstallDeps) {
  & $PythonExe -m pip install -r .\backend\requirements.txt
  if ($LASTEXITCODE -ne 0) { throw "Failed to install backend requirements." }
}

$env:PYTHONPATH = (Resolve-Path ".\backend").Path
& $PythonExe -m pytest .\backend\tests -q
if ($LASTEXITCODE -ne 0) { throw "Backend tests failed." }
