@echo off
SETLOCAL EnableDelayedExpansion
for %%a in (
	EnhancedPowerManagementEnabled
	AllowIdleIrpInD3
	EnableSelectiveSuspend
	DeviceSelectiveSuspended
	D3ColdSupported
	SelectiveSuspendEnabled
	SelectiveSuspendOn
	SelectiveSuspendTimeout
	WaitWakeEnabled
	WdfDirectedPowerTransitionEnable
	EnableIdlePowerManagement
	IdleInWorkingState
	WakeEnabled
	IdleTimeoutPeriodInMilliSec
	IdleTimeoutInMS
	MinimumIdleTimeoutInMS
) do for /f "delims=" %%b in ('reg query "HKLM\SYSTEM\CurrentControlSet\Enum" /s /f "%%a" ^| findstr "HKEY"') do reg delete "%%b" /v "%%a" /f

bcdedit /set disabledynamictick yes

reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v EnergyEstimationEnabled /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v IdleProcessorsRequireQosManagement /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v PlatformRoleOverride /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v PlatformAoAcOverride /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v MSDisabled /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v CoalescingFlushInterval /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v CoalescingTimerInterval /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v EventProcessorEnabled /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\stornvme\Parameters\Device" /v IdlePowerMode /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\stornvme\Parameters\Device" /v DisableDSTThrottle /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Classpnp" /v NVMeDisablePerfThrottling /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Storage" /v StorageD3InModernStandby /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\usbflags" /v Allow64KLowOrFullSpeedControlTransfers /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\usbflags" /v DisableHCS0Idle /f

powershell "Set-CimInstance -Query 'SELECT InstanceName FROM MSPower_DeviceWakeEnable WHERE (Enable = False)' -Namespace 'root\WMI' -Property @{Enable = $true}"
powershell "Set-CimInstance -Query 'SELECT InstanceName FROM MSPower_DeviceEnable WHERE (Enable = False)' -Namespace 'root\WMI' -Property @{Enable = $true}"
for %%a in (EnableHIPM EnableDIPM EnableHDDParking) do for /f "delims=" %%b in ('reg query "HKLM\SYSTEM\CurrentControlSet\Services" /s /f "%%a" ^| findstr "HKEY"') do reg delete "%%b" /v "%%a" /f
for /f "tokens=*" %%s in ('reg query "HKLM\SYSTEM\CurrentControlSet\Enum" /s /f "StorPort" ^| findstr /e "StorPort"') do (
    reg delete "%%s" /v "EnableIdlePowerManagement" /f
	reg delete "%%s" /v "DisableRuntimePowerManagement" /f
    reg delete "%%s" /v "DisableD3Cold" /f
)

reg add "HKLM\SYSTEM\CurrentControlSet\Services\WmiAcpi" /v "Start" /t REG_DWORD /d "3" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\AcpiPmi" /v "Start" /t REG_DWORD /d "3" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\acpitime" /v "Start" /t REG_DWORD /d "3" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\GpuEnergyDrv" /v "Start" /t REG_DWORD /d "3" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\GraphicsPerfSvc" /v "Start" /t REG_DWORD /d "3" /f