@echo off
setlocal EnableDelayedExpansion
netsh int ip reset >nul 2>&1
netsh interface ipv4 reset >nul 2>&1
netsh interface ipv6 reset >nul 2>&1
netsh interface tcp reset >nul 2>&1
netsh winsock reset >nul 2>&1
netsh winsock reset catalog >nul 2>&1
ipconfig /release >nul 2>&1
ipconfig /renew >nul 2>&1
ipconfig /flushdns >nul 2>&1

for /f "tokens=3,4*" %%a in ('route print -4 ^| findstr /r /c:"^ *0\.0\.0\.0 *0\.0\.0\.0"') do set "ifidx=%%b"
for /f "skip=3 tokens=1,4*" %%a in ('netsh interface ipv4 show interfaces') do if "%%a"=="!ifidx!" set "iface=%%b"
if not defined iface (
    for /f "skip=3 tokens=4,5*" %%a in ('netsh interface ipv4 show interfaces') do (
        if /i "%%a"=="connected" if not defined iface echo %%b | findstr /i "loopback" >nul || set "iface=%%b"
    )
)
if not defined iface exit /b 1
 
set "dest=1.1.1.1"
set /a low=1280, high=1472, best=1280
 
:bsearch
if !low! gtr !high! goto done
set /a mid=(!low!+!high!)/2
set /a ok=0
for /l %%i in (1,1,3) do ping -n 1 -w 1000 -f -l !mid! !dest! >nul 2>&1 && set /a ok+=1
if !ok! geq 2 (set /a best=!mid!, low=!mid!+1) else set /a high=!mid!-1
goto bsearch
 
:done
set /a finalMTU=!best!+28
netsh interface ipv4 set subinterface "!iface!" mtu=!finalMTU! store=persistent >nul
echo Interface: !iface! ^| MTU set to !finalMTU! (payload !best!)

for /f "tokens=*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}" /v "*SpeedDuplex" /s 2^>nul ^| findstr "HKEY"') do (
    echo NIC: %%a
    
    reg add "%%a" /v "EnablePME" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "EnableSavePowerNow" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*EnableDynamicPowerGating" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*DeviceSleepOnDisconnect" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*EEE" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*ModernStandbyWoLMagicPacket" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*SelectiveSuspend" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "AutoPowerSaveModeEnabled" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "EEELinkAdvertisement" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "EeePhyEnable" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "EnableGreenEthernet" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "EnableModernStandby" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*EncapsulatedPacketTaskOffloadNvgre" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*EncapsulatedPacketTaskOffloadVxlan" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*EncapsulatedPacketTaskOffload" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "GigaLite" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "PowerDownPll" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "PowerSavingMode" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "ReduceSpeedOnPowerDown" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "SavePowerNowEnabled" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "ULPMode" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "EnablePowerManagement" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "EnableD3ColdInS0" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "AdvancedEEE" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "EnableAspm" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "ASPM" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "OBFFEnabled" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "DMACoalescing" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "ITR" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "TxIntDelay" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "TxDelay" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*WakeOnMagicPacket" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*WakeOnPattern" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "WakeOnLink" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "WakeOnSlot" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "WakeUpModeCap" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "S5WakeOnLan" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "S0MgcPkt" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "LatencyToleranceReporting" /t REG_SZ /d "0" /f 2>nul	
    reg add "%%a" /v "ForceWakeFromMagicPacketOnModernStandby" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "WakeFromS5" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "WakeOn" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "WakeFromPowerOff" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "WolShutdownLinkSpeed" /t REG_SZ /d "2" /f 2>nul
    reg add "%%a" /v "WakeOnMagicPacketFromS5" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*PMNSOffload" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*PMARPOffload" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*NicAutoPowerSaver" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*TCPChecksumOffloadIPv4" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*TCPChecksumOffloadIPv6" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*TCPConnectionOffloadIPv4" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*TCPConnectionOffloadIPv6" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*TCPUDPChecksumOffloadIPv4" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*TCPUDPChecksumOffloadIPv6" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*UDPChecksumOffloadIPv4" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*UDPChecksumOffloadIPv6" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*IPChecksumOffloadIPv4" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*UdpRsc" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*UsoIPv4" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*UsoIPv6" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*RscIPv4" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*RscIPv6" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*IPsecOffloadV1IPv4" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*IPsecOffloadV2IPv4" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*IPsecOffloadV2" /t REG_SZ /d "3" /f 2>nul
    reg add "%%a" /v "*LsoV1IPv4" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*LsoV2IPv4" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*LsoV2IPv6" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "TeredoOffload" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*QoSOffload" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*RSS" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*NumRssQueues" /t REG_SZ /d "1" /f 2>nul
    reg add "%%a" /v "*RssBaseProcNumber" /t REG_SZ /d "2" /f 2>nul
    reg add "%%a" /v "*FlowControl" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "WaitAutoNegComplete" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*InterruptModeration" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "LogLinkStateEvent" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "*PriorityVLANTag" /t REG_SZ /d "0" /f 2>nul
    reg add "%%a" /v "PnPCapabilities" /t REG_DWORD /d "24" /f 2>nul
)

powershell "disable-netadapterbinding -name "*" -componentid ms_lldp, ms_lltdio, ms_implat, ms_rspndr, ms_server, ms_msclient"
powershell "Set-NetOffloadGlobalSetting -PacketCoalescingFilter Disabled -ErrorAction SilentlyContinue"
powershell "Set-NetOffloadGlobalSetting -ReceiveSegmentCoalescing Enabled -ErrorAction SilentlyContinue"
netsh int udp set global uro=enabled
netsh int tcp set security profiles=disabled
netsh int tcp set global timestamps=disabled
netsh int tcp set global autotuninglevel=normal
netsh int tcp set heuristics disabled

reg add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "DefaultPnPCapabilities" /t REG_DWORD /d "24" /f

reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\QoS" /v "Do not use NLA" /t REG_SZ /d "1" /f

reg add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "TrackNblOwner" /t REG_DWORD /d "0" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "DisableNDISWatchDog" /t REG_DWORD /d "1" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "DisableNaps" /t REG_DWORD /d "1" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "DebugLoggingMode" /t REG_DWORD /d "0" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "NoPauseOnSuspend" /t REG_DWORD /d "1" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "DisableWDIWatchdogForceBugcheck" /t REG_DWORD /d "1" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "DisableReenumerationTimeoutBugcheck" /t REG_DWORD /d "1" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\NDIS\Parameters" /v "EnableNicAutoPowerSaverInSleepStudy" /t REG_DWORD /d "0" /f

reg add "HKLM\SYSTEM\CurrentControlSet\Services\NetBT\Parameters" /v "EnableLMHOSTS" /t REG_DWORD /d "0" /f

reg add "HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /v "TcpAckFrequency" /t REG_DWORD /d "1" /f
reg add "HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /v "TcpDelAckTicks" /t REG_DWORD /d "0" /f

reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WcmSvc\Local" /v "fDisablePowerManagement" /t REG_DWORD /d "1" /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WcmSvc\GroupPolicy" /v "fDisablePowerManagement" /t REG_DWORD /d "1" /f

reg add "HKLM\System\CurrentControlSet\Services\Dnscache\Parameters" /v "DisableCoalescing" /t REG_DWORD /d "1" /f

for /f "skip=3 tokens=1" %%I in ('netsh interface ipv4 show interfaces') do (
    netsh interface ipv4 set dnsservers name=%%I static 1.1.1.1 primary
    netsh interface ipv4 add dnsservers name=%%I 1.0.0.1 index=2
)

for /f "delims=" %%u in ('reg query "HKLM\SYSTEM\CurrentControlSet\Services\NetBT\Parameters\Interfaces" /s /f "NetbiosOptions" ^| findstr "HKEY"') do (
    reg add "%%u" /v "NetbiosOptions" /t REG_DWORD /d "2" /f
)

netsh int ipv4 set gl loopbacklargemtu=disabled
netsh int ipv6 set gl loopbacklargemtu=disabled
netsh int tcp set supplemental Template=Internet CongestionProvider=BBR2
netsh int tcp set supplemental Template=Datacenter CongestionProvider=BBR2
netsh int tcp set supplemental Template=Compat CongestionProvider=BBR2
netsh int tcp set supplemental Template=DatacenterCustom CongestionProvider=BBR2
netsh int tcp set supplemental Template=InternetCustom CongestionProvider=BBR2
netsh int tcp set supplemental Template=Automatic CongestionProvider=BBR2