$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
  throw "Missing virtual environment. Run .\scripts\setup_backend.ps1 first. Expected: $PythonExe"
}

$BackendDir = Join-Path $RepoRoot "backend"
Push-Location $BackendDir
try {
  & $PythonExe -m uvicorn extractor_service.main:app --reload --host 0.0.0.0 --port 8001
} finally {
  Pop-Location
}
