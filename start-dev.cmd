@echo off
setlocal

set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

where npm >nul 2>&1
if errorlevel 1 (
  echo [ERROR] npm is not available in PATH.
  echo Install Node.js and reopen your terminal.
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [ERROR] Missing virtual environment at .venv\Scripts\python.exe
  echo Run .\scripts\setup_backend.ps1 first.
  exit /b 1
)

if not exist "scripts\run_extractor.ps1" (
  echo [ERROR] scripts\run_extractor.ps1 not found.
  exit /b 1
)

if not exist "scripts\run_api.ps1" (
  echo [ERROR] scripts\run_api.ps1 not found.
  exit /b 1
)

if not exist "frontend\package.json" (
  echo [ERROR] frontend\package.json not found.
  exit /b 1
)

echo Starting extractor, API, and frontend in separate terminals...
start "Chat App Extractor" powershell -NoExit -ExecutionPolicy Bypass -File "%ROOT_DIR%scripts\run_extractor.ps1"
start "Chat App API" powershell -NoExit -ExecutionPolicy Bypass -File "%ROOT_DIR%scripts\run_api.ps1"
start "Chat App Frontend" cmd /k "cd /d ""%ROOT_DIR%frontend"" && npm run dev"

echo.
echo Frontend:  http://localhost:5173
echo API:       http://localhost:8000
echo Extractor: http://localhost:8001
echo.
echo Close each terminal window to stop its server.

endlocal
