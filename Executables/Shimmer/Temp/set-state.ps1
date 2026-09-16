param(
    [string[]] $Set,
    [switch]   $List
)

$File = "C:\Shimmer\Software\tweakdata.json"

if (-not (Test-Path $File)) { Write-Error "File not found: $File"; exit 1 }

$raw  = [System.IO.File]::ReadAllText($File)
$data = $raw | ConvertFrom-Json

if ($List) {
    $data.PSObject.Properties | ForEach-Object {
        Write-Host "[$($_.Value)] $($_.Name)"
    }
    exit 0
}

if (-not $Set) { Write-Host "Usage: -Set Key=0|1 or -List"; exit 0 }

foreach ($p in ($Set -join ',') -split ',' | Where-Object { $_ -match '\S' }) {
    if ($p -notmatch '^(.+)=([01])$') { Write-Warning "Invalid: '$p'"; continue }

    $key  = $Matches[1].Trim()
    $val  = [int]$Matches[2]
    $prop = $data.PSObject.Properties[$key]

    if (-not $prop) { Write-Warning "Unknown key '$key'"; continue }

    Write-Host "$($prop.Name): $($prop.Value) -> $val"
    $raw = $raw -replace "(`"$([regex]::Escape($key))`":\s*)\d", "`${1}$val"
}

[System.IO.File]::WriteAllText($File, $raw, (New-Object System.Text.UTF8Encoding $false))