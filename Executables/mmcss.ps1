Get-CimInstance Win32_NetworkAdapter | Where-Object PNPDeviceID -like "PCI\VEN_*" | ForEach-Object {
    $driver = (Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Enum\$($_.PNPDeviceID)" Driver -EA 0).Driver
    if (-not $driver) { return }

    $ndi = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\$driver\Ndi"
    $svc = ((Get-ItemProperty $ndi Service -EA 0).Service) -replace '\.$'
    if (-not $svc) { return }

    $svcPath = "HKLM:\SYSTEM\CurrentControlSet\Services\$svc"
    $isKmdf = Test-Path "$svcPath\Parameters\Wdf"
    $isUmdf = Test-Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\WUDF\Services\$svc\Parameters\Wdf"

    if ($isKmdf -or $isUmdf) {
        Write-Host "NetAdapterCx: $($_.Name)"
		New-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" -Name "SystemResponsiveness" -PropertyType DWord -Value 100 -Force
        New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\MMCSS" -Name "Start" -PropertyType DWord -Value 4 -Force
		C:\Shimmer\Temp\set-state.ps1 -Set MMCSS=0 -ErrorAction SilentlyContinue
    } elseif (Test-Path $ndi) {
        Write-Host "NDIS: $($_.Name)"
    }
}