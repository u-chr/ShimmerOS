Get-ChildItem -Path "$env:TEMP" | Where-Object { $_.Name -ne 'AME' } | Remove-Item -Force -Recurse
Remove-Item -Path "$([Environment]::GetFolderPath('Windows'))\Temp\*" -Force -Recurse
Remove-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband" -Force -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "$env:APPDATA\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\*" -Force -Recurse -ErrorAction SilentlyContinue

Get-ChildItem "$env:LOCALAPPDATA\Packages" -Directory |
    Where-Object { $_.Name -match "Microsoft.Windows.StartMenuExperienceHost" } |
    ForEach-Object {
        Remove-Item "$env:LOCALAPPDATA\Packages\$($_.Name)\LocalState" -Recurse -Force -ErrorAction SilentlyContinue
    }

Get-ChildItem "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultAccount" -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "start.tilegrid" } |
    Remove-Item -Force
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Start" -Name Config -Force -ErrorAction SilentlyContinue

Remove-Item "C:\Shimmer\Temp" -Recurse -Force -ErrorAction SilentlyContinue