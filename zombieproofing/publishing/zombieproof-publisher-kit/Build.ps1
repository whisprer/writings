param(
    [ValidateSet('all','radio','computers','engines','water')][string]$Book = 'all',
    [string]$Config = 'publishing-details.json',
    [string]$Output = 'finished',
    [ValidateSet('msedge','chrome','')][string]$BrowserChannel = '',
    [switch]$Check
)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$venvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $venvPython)) {
    Write-Error 'Run .\Setup.ps1 first.'
    exit 1
}
$arguments = @('publish.py', '--config', $Config, '--book', $Book, '--output', $Output)
if ($Check) { $arguments += '--check' }
if ($BrowserChannel) { $arguments += @('--browser-channel', $BrowserChannel) }
& $venvPython @arguments
exit $LASTEXITCODE
