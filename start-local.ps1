[CmdletBinding()]
param(
    [switch]$Production,
    [switch]$Offline
)

$ErrorActionPreference = 'Stop'
$workspacePath = $PSScriptRoot
$pythonPath = Join-Path $workspacePath '.venv\Scripts\python.exe'
$frontendPath = Join-Path $workspacePath 'frontend'
$logPath = Join-Path $workspacePath '.local-logs'

if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Python environment is missing. Run: python -m venv .venv; .\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt'
}
if (-not (Test-Path -LiteralPath (Join-Path $frontendPath 'node_modules'))) {
    throw 'Frontend dependencies are missing. Run: Set-Location frontend; npm ci'
}
New-Item -ItemType Directory -Path $logPath -Force | Out-Null
if ($Offline) { $env:PLANNER_MODE = 'offline' }

function Test-LocalPort([int]$Port) {
    $client = New-Object System.Net.Sockets.TcpClient
    try { $client.Connect('127.0.0.1', $Port); return $true }
    catch { return $false }
    finally { $client.Dispose() }
}

$processRecords = @()
if (-not (Test-LocalPort 8000)) {
    $backendProcess = Start-Process -FilePath $pythonPath -ArgumentList @(
        '-m', 'uvicorn', 'backend.app.main:app', '--host', '127.0.0.1', '--port', '8000'
    ) -WorkingDirectory $workspacePath -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $logPath 'backend.out.log') `
        -RedirectStandardError (Join-Path $logPath 'backend.err.log')
    $processRecords += @{ service = 'backend'; id = $backendProcess.Id }
}

if (-not (Test-LocalPort 3000)) {
    $nodePath = (Get-Command node.exe).Source
    $nextPath = Join-Path $frontendPath 'node_modules\next\dist\bin\next'
    $nextMode = if ($Production) { 'start' } else { 'dev' }
    $nextArguments = @('"' + $nextPath + '"', $nextMode, '--hostname', '127.0.0.1', '--port', '3000')
    if (-not $Production) { $nextArguments += '--webpack' }
    $frontendProcess = Start-Process -FilePath $nodePath -ArgumentList $nextArguments `
        -WorkingDirectory $frontendPath -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $logPath 'frontend.out.log') `
        -RedirectStandardError (Join-Path $logPath 'frontend.err.log')
    $processRecords += @{ service = 'frontend'; id = $frontendProcess.Id }
}

# Keep the records of previously started processes when the script is run again.
$statePath = Join-Path $workspacePath '.local-services.json'
$previousRecords = @()
if (Test-Path -LiteralPath $statePath) {
    try { $previousRecords = @(Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json) }
    catch { $previousRecords = @() }
}
$flatRecords = @()
foreach ($record in $previousRecords) {
    if ($record.id) { $flatRecords += $record }
    elseif ($record.value) {
        foreach ($nested in $record.value) { if ($nested.id) { $flatRecords += $nested } }
    }
}
foreach ($record in $processRecords) { $flatRecords += $record }
ConvertTo-Json -InputObject @($flatRecords) -Depth 3 | Set-Content -LiteralPath $statePath

$ready = $false
for ($attempt = 0; $attempt -lt 60; $attempt++) {
    if ((Test-LocalPort 8000) -and (Test-LocalPort 3000)) { $ready = $true; break }
    Start-Sleep -Seconds 1
}
if (-not $ready) { throw 'A local service did not start. Inspect .local-logs\*.err.log.' }

Write-Host 'Dashboard: http://localhost:3000'
Write-Host 'Backend:   http://localhost:8000/api/health'
Write-Host 'API docs:  http://localhost:8000/docs'
Write-Host 'Logs:      .local-logs'
Write-Host 'WhatsApp previews are safe; this script does not enable or send live notifications.'
