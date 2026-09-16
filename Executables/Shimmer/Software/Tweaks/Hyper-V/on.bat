@echo off
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v RequirePlatformSecurityFeatures /f
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v LsaCfgFlags /f
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v HVCIMATRequired /f
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v EnableVirtualizationBasedSecurity /f
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v HypervisorEnforcedCodeIntegrity /f
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v ConfigureSystemGuardLaunch /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v Enabled /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v WasEnabledBy /t REG_DWORD /d 1 /f
DISM /Online /Enable-Feature:Microsoft-Hyper-V-All /Quiet /NoRestart
DISM /Online /Enable-Feature:VirtualMachinePlatform /Quiet /NoRestart
DISM /Online /Enable-Feature:HypervisorPlatform /Quiet /NoRestart
sc config hyperkbd start= system
sc config hypervideo start= system
sc config gencounter start= auto
sc config hvservice start= auto
sc config hvcrash start= system
sc config HvHost start= auto
sc config uevagentservice start= auto
sc config uevagentdriver start= system
sc config appvclient start= auto
sc config bttflt start= auto
sc config vid start= auto
powershell "Get-PnpDevice -FriendlyName 'Microsoft Hyper-V Virtualization Infrastructure Driver' -ErrorAction Ignore | Enable-PnpDevice -Confirm:$false -ErrorAction Ignore"
echo
echo error here is okay :D - loplxl