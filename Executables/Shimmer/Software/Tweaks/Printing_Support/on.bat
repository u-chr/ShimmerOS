@echo off
SETLOCAL EnableDelayedExpansion
title Printing configuration

for %%z in (
	PrintWorkFlowUserSvc
	StiSvc
	PrintNotify
	usbprint
	McpManagementService
	PrintScanBrokerService
	PrintDeviceConfigurationService
) do (
reg add "HKLM\SYSTEM\CurrentControlSet\Services\%%z" /v "Start" /t REG_DWORD /d "3" /f
)
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Spooler" /v "Start" /t REG_DWORD /d "2" /f
reg add "HKCR\SystemFileAssociations\image\shell\print\command" /ve /t REG_EXPAND_SZ /d "%%SystemRoot%%\System32\rundll32.exe \"%%ProgramFiles%%\Windows Photo Viewer\PhotoViewer.dll\", ImageView_Fullscreen %%1" /f >nul 2>&1
reg add "HKCR\SystemFileAssociations\image\shell\print\DropTarget" /v "Clsid" /t REG_SZ /d "{60fd46de-f830-4894-a628-6fa81bc0190d}" /f >nul 2>&1
reg add "HKCR\batfile\shell\print\command" /ve /t REG_EXPAND_SZ /d "%%SystemRoot%%\System32\NOTEPAD.EXE /p %%1" /f >nul 2>&1
reg add "HKCR\htmlfile\shell\print\command" /ve /t REG_EXPAND_SZ /d "\"%%systemroot%%\system32\rundll32.exe\" \"%%systemroot%%\system32\mshtml.dll\",PrintHTML \"%%1\"" /f >nul 2>&1
reg add "HKCR\JSEFile\Shell\Print\Command" /ve /t REG_SZ /d "C:\Windows\System32\Notepad.exe /p %%1" /f >nul 2>&1
reg add "HKCR\otffile\shell\print\command" /ve /t REG_EXPAND_SZ /d "%%SystemRoot%%\System32\fontview.exe /p %%1" /f >nul 2>&1
reg add "HKCR\pfmfile\shell\print\command" /ve /t REG_EXPAND_SZ /d "%%SystemRoot%%\System32\fontview.exe /p %%1" /f >nul 2>&1
reg add "HKCR\regfile\shell\print\command" /ve /t REG_EXPAND_SZ /d "%%SystemRoot%%\system32\notepad.exe /p \"%%1\"" /f >nul 2>&1
reg add "HKCR\ttcfile\shell\print\command" /ve /t REG_EXPAND_SZ /d "%%SystemRoot%%\System32\fontview.exe /p %%1" /f >nul 2>&1
reg add "HKCR\ttffile\shell\print\command" /ve /t REG_EXPAND_SZ /d "%%SystemRoot%%\System32\fontview.exe /p %%1" /f >nul 2>&1
reg add "HKCR\VBEFile\Shell\Print\Command" /ve /t REG_EXPAND_SZ /d "\"%%SystemRoot%%\System32\Notepad.exe\" /p %%1" /f >nul 2>&1
reg add "HKCR\VBSFile\Shell\Print\Command" /ve /t REG_EXPAND_SZ /d "\"%%SystemRoot%%\System32\Notepad.exe\" /p %%1" /f >nul 2>&1
reg add "HKCR\WSFFile\Shell\Print\Command" /ve /t REG_EXPAND_SZ /d "\"%%SystemRoot%%\System32\Notepad.exe\" /p %%1" /f >nul 2>&1
DISM.exe /Online /Enable-Feature /FeatureName:"Printing-PrintToPDFServices-Features" /NoRestart >nul 2>&1
DISM.exe /Online /Enable-Feature /FeatureName:"Printing-Foundation-Features" /NoRestart >nul 2>&1
DISM.exe /Online /Enable-Feature /FeatureName:"Printing-Foundation-InternetPrinting-Client" /NoRestart >nul 2>&1