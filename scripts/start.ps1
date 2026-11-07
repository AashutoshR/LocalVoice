$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    py -3.13 -m venv .venv
    & .\.venv\Scripts\python.exe -m pip install -e '.[dev]'
}
& .\.venv\Scripts\localvoice.exe serve
