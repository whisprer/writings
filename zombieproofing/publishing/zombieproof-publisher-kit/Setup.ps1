param([switch]$UseInstalledBrowser)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Command failed: $Program (exit $LASTEXITCODE)" }
}
try {
    $venvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path $venvPython)) {
        if (Get-Command py -ErrorAction SilentlyContinue) {
            Invoke-Checked 'py' @('-3', '-c', 'import sys; assert sys.version_info >= (3,12), "Python 3.12 or newer is required"')
            Invoke-Checked 'py' @('-3', '-m', 'venv', '.venv')
        } elseif (Get-Command python -ErrorAction SilentlyContinue) {
            Invoke-Checked 'python' @('-c', 'import sys; assert sys.version_info >= (3,12), "Python 3.12 or newer is required"')
            Invoke-Checked 'python' @('-m', 'venv', '.venv')
        } else {
            throw 'Install native Windows Python 3.12 or newer, including its Python launcher, then run Setup.ps1 again.'
        }
    }
    Invoke-Checked $venvPython @('-m', 'pip', 'install', '-r', 'requirements.txt')
    if (-not $UseInstalledBrowser) {
        Invoke-Checked $venvPython @('-m', 'playwright', 'install', 'chromium')
    }
    Write-Host 'Setup complete. Edit publishing-details.json, add your imprint image, then run .\Build.ps1.'
} catch {
    Write-Error $_
    exit 1
}
