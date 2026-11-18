[CmdletBinding()]
param([switch]$BackendOnly)
$ErrorActionPreference = 'Stop'
$workspacePath = $PSScriptRoot
$statePath = Join-Path $workspacePath '.local-services.json'
if (-not (Test-Path -LiteralPath $statePath)) { Write-Host 'No script-owned local processes recorded.'; return }
$storedRecords = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
$records = @()
foreach ($record in $storedRecords) {
    if ($record.id) { $records += $record }
    elseif ($record.value) {
        foreach ($nested in $record.value) { if ($nested.id) { $records += $nested } }
    }
}
$remaining = @()
foreach ($record in $records) {
    if (-not $record.id) { continue }
    if ($BackendOnly -and $record.service -ne 'backend') { $remaining += $record; continue }
    $ownedProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $($record.id)" -ErrorAction SilentlyContinue
    if (-not $ownedProcess) {
        $stillRunning = Get-Process -Id $record.id -ErrorAction SilentlyContinue
        if ($stillRunning) {
            Write-Warning "Cannot inspect process $($record.id); it was preserved. Run from your normal PowerShell account."
            $remaining += $record
        }
        continue
    }
    $commandLine = [string]$ownedProcess.CommandLine
    $executable = [string]$ownedProcess.ExecutablePath
    $expectedPython = Join-Path $workspacePath '.venv\Scripts\python.exe'
    $expectedNext = Join-Path $workspacePath 'frontend\node_modules\next\dist\bin\next'
    $isBackend = $record.service -eq 'backend' -and $executable -eq $expectedPython -and $commandLine.Contains('backend.app.main:app')
    $isFrontend = $record.service -eq 'frontend' -and $commandLine.Contains($expectedNext)
    if (-not ($isBackend -or $isFrontend)) {
        Write-Warning "Process $($record.id) does not match this workspace; it was preserved."
        $remaining += $record
        continue
    }
    # The parent identity was verified before stopping its descendants.
    $children = @(Get-CimInstance Win32_Process -Filter "ParentProcessId = $($record.id)" -ErrorAction SilentlyContinue)
    foreach ($child in $children) { Stop-Process -Id $child.ProcessId -Force -ErrorAction SilentlyContinue }
    Stop-Process -Id $record.id -Force -ErrorAction SilentlyContinue
    Write-Host "Stopped script-owned $($record.service) process $($record.id)."
}
ConvertTo-Json -InputObject @($remaining) -Depth 3 | Set-Content -LiteralPath $statePath
