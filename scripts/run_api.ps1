$ErrorActionPreference = "Stop"

$PythonExe = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
  throw "Missing virtual environment. Run .\scripts\setup_backend.ps1 first."
}

Push-Location .\backend
try {
  & $PythonExe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
} finally {
  Pop-Location
}

