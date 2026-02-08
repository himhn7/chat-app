param(
  [switch]$InstallDeps
)

$ErrorActionPreference = "Stop"

Push-Location .\frontend
try {
  if ($InstallDeps -or -not (Test-Path ".\node_modules")) {
    npm install
    if ($LASTEXITCODE -ne 0) { throw "npm install failed." }
  }
  npm run test:smoke
  if ($LASTEXITCODE -ne 0) { throw "Frontend smoke test failed." }
} finally {
  Pop-Location
}
