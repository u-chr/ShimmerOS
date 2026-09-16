@echo off
setlocal EnableDelayedExpansion

set "base=HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
set "target="

for /f "tokens=*" %%A in ('reg query "%base%" /k /f "*" ^| findstr /r "\\....$"') do (
    reg query "%%A" /v "ProviderName" 2>nul | find /i "Advanced Micro Devices, Inc." >nul
    if !errorlevel! equ 0 (
        set "target=%%A"
    )
)

reg delete "%target%" /v "ReportAnalytics" /f >nul 2>&1
reg delete "%target%" /v "NotifySubscription" /f >nul 2>&1
reg delete "%target%" /v "AllowSubscription" /f >nul 2>&1
reg delete "%target%" /v "ShowReleaseNotes" /f >nul 2>&1

reg delete "%target%" /v "StutterMode" /f >nul 2>&1
reg delete "%target%" /v "KMD_EnableAmdFendrOptions" /f >nul 2>&1
reg delete "%target%" /v "KMD_ChillEnabled" /f >nul 2>&1
reg delete "%target%" /v "KMD_DeLagEnabled" /f >nul 2>&1
reg delete "%target%" /v "KMD_FramePacingSupport" /f >nul 2>&1
reg delete "%target%" /v "KMD_RadeonBoostEnabled" /f >nul 2>&1
reg delete "%target%" /v "DalDisableStutter" /f >nul 2>&1
reg delete "%target%" /v "DisableBlockWrite" /f >nul 2>&1
reg delete "%target%" /v "DisableFBCSupport" /f >nul 2>&1
reg delete "%target%" /v "DisableFBCForFullScreenApp" /f >nul 2>&1

reg delete "%target%" /v "PP_Force3DPerformanceMode" /f >nul 2>&1
reg delete "%target%" /v "PP_ForceHighDPMLevel" /f >nul 2>&1
reg delete "%target%" /v "PP_SclkDeepSleepDisable" /f >nul 2>&1
reg delete "%target%" /v "PP_GfxOffControl" /f >nul 2>&1
reg delete "%target%" /v "PP_ThermalAutoThrottlingEnable" /f >nul 2>&1
reg delete "%target%" /v "PP_EnableRaceToIdle" /f >nul 2>&1

reg delete "%target%" /v "EnableUlps" /f >nul 2>&1
reg delete "%target%" /v "EnableUlps_NA" /f >nul 2>&1
reg delete "%target%" /v "PP_DisableULPS" /f >nul 2>&1
reg delete "%target%" /v "KMD_EnableULPS" /f >nul 2>&1
reg delete "%target%" /v "KMD_ForceD3ColdSupport" /f >nul 2>&1

reg delete "%target%" /v "EnableAspmL0s" /f >nul 2>&1
reg delete "%target%" /v "EnableAspmL1" /f >nul 2>&1
reg delete "%target%" /v "EnableAspmL1SS" /f >nul 2>&1
reg delete "%target%" /v "DisableAspmL0s" /f >nul 2>&1
reg delete "%target%" /v "DisableAspmL1" /f >nul 2>&1

reg delete "%target%" /v "DisableGfxClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableVceClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableSamuClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableRomMGCGClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableGfxCoarseGrainClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableGfxMediumGrainClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableGfxFineGrainClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableHdpMGClockGating" /f >nul 2>&1
reg delete "%target%" /v "EnableVceSwClockGating" /f >nul 2>&1
reg delete "%target%" /v "EnableUvdClockGating" /f >nul 2>&1
reg delete "%target%" /v "EnableGfxClockGatingThruSmu" /f >nul 2>&1
reg delete "%target%" /v "EnableSysClockGatingThruSmu" /f >nul 2>&1
reg delete "%target%" /v "DisableXdmaSclkGating" /f >nul 2>&1
reg delete "%target%" /v "DalFineGrainClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableRomMediumGrainClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableNbioMediumGrainClockGating" /f >nul 2>&1
reg delete "%target%" /v "DisableMcMediumGrainClockGating" /f >nul 2>&1
reg delete "%target%" /v "IRQMgrDisableIHClockGating" /f >nul 2>&1

reg delete "%target%" /v "DisableGfxMGLS" /f >nul 2>&1
reg delete "%target%" /v "DisableHdpClockPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableUVDPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableVCEPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableAcpPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableDrmdmaPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableGfxCGPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableStaticGfxMGPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableDynamicGfxMGPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableCpPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableGDSPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableXdmaPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableGFXPipelinePowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisableQuickGfxMGPowerGating" /f >nul 2>&1
reg delete "%target%" /v "DisablePowerGating" /f >nul 2>&1

reg delete "%target%" /v "SMU_DisableMmhubPowerGating" /f >nul 2>&1
reg delete "%target%" /v "SMU_DisableAthubPowerGating" /f >nul 2>&1

reg delete "%target%" /v "DalForceMaxDisplayClock" /f >nul 2>&1
reg delete "%target%" /v "DalDisableClockGating" /f >nul 2>&1
reg delete "%target%" /v "DalDisableDeepSleep" /f >nul 2>&1
reg delete "%target%" /v "DalDisableDiv2" /f >nul 2>&1

reg delete "%target%" /v "EnableSpreadSpectrum" /f >nul 2>&1
reg delete "%target%" /v "EnableVcePllSpreadSpectrum" /f >nul 2>&1

set "Root=HKLM\System\CurrentControlSet\Services"

for %%S in ("AMD Crash Defender Service" "amdfendr" "amdfendrmgr" "amdlog") do (
    reg query "%Root%\%%~S" >nul 2>&1 && Reg add "%Root%\%%~S" /v "Start" /t REG_DWORD /d "2" /f >nul 2>&1
)
