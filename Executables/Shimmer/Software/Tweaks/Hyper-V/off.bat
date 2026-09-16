@echo off
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v RequirePlatformSecurityFeatures /t REG_DWORD /d 1 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v LsaCfgFlags /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v HVCIMATRequired /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v EnableVirtualizationBasedSecurity /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v HypervisorEnforcedCodeIntegrity /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v ConfigureSystemGuardLaunch /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v WasEnabledBy /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v Enabled /t REG_DWORD /d 0 /f
DISM /Online /Disable-Feature:Microsoft-Hyper-V-All /Quiet /NoRestart
DISM /Online /Disable-Feature:VirtualMachinePlatform /Quiet /NoRestart
DISM /Online /Disable-Feature:HypervisorPlatform /Quiet /NoRestart
sc config hyperkbd start= disabled
sc config hypervideo start= disabled
sc config gencounter start= disabled
sc config hvservice start= disabled
sc config hvcrash start= disabled
sc config HvHost start= disabled
sc config uevagentservice start= disabled
sc config uevagentdriver start= disabled
sc config appvclient start= disabled
sc config bttflt start= disabled
sc config vid start= disabled
powershell "Get-PnpDevice -FriendlyName 'Microsoft Hyper-V Virtualization Infrastructure Driver' -ErrorAction Ignore | Disable-PnpDevice -Confirm:$false -ErrorAction Ignore"
echo
echo error here is okay :D - loplxl