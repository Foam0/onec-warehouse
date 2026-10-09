param(
    [Parameter(Mandatory=$true)][string]$Platform,
    [string]$DatabasePath = (Join-Path $PSScriptRoot "../build/infobase")
)
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path $PSScriptRoot -Parent
$SourcePath = Join-Path $ProjectRoot "src"
$BuildPath = Join-Path $ProjectRoot "build"
if (-not (Test-Path -LiteralPath $Platform -PathType Leaf)) { throw "1cv8 executable not found" }
$DatabasePath = [IO.Path]::GetFullPath($DatabasePath)
if (Test-Path -LiteralPath $DatabasePath) {
    throw "Choose a new directory. Existing infobases are never overwritten: $DatabasePath"
}
New-Item -ItemType Directory -Force -Path $BuildPath | Out-Null
function Invoke-DesignerStep([string]$Name, [string[]]$StepArguments) {
    $LogPath = Join-Path $BuildPath "$Name.log"
    & $Platform @StepArguments /DisableStartupDialogs /Out $LogPath
    if ($LASTEXITCODE -ne 0) { throw "1C failed ($LASTEXITCODE). See $LogPath" }
    if (Test-Path $LogPath) { Get-Content $LogPath }
}
Invoke-DesignerStep "create" @("CREATEINFOBASE", ('File="' + $DatabasePath + '";'))
Invoke-DesignerStep "import" @("DESIGNER", "/F", $DatabasePath,
    "/LoadConfigFromFiles", $SourcePath, "-Format", "Hierarchical")
Invoke-DesignerStep "update" @("DESIGNER", "/F", $DatabasePath, "/UpdateDBCfg")
Invoke-DesignerStep "check" @("DESIGNER", "/F", $DatabasePath, "/CheckConfig",
    "-ThinClient", "-Server", "-ExternalConnection")
Write-Host "Review build/check.log. Then open this infobase in Designer and create an administrator."
Write-Host "Infobase: $DatabasePath"
