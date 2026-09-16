@echo off
SETLOCAL EnableDelayedExpansion
title Printing configuration

for %%z in (
	Spooler
	PrintWorkFlowUserSvc
	StiSvc
	PrintNotify
	usbprint
	McpManagementService
	PrintScanBrokerService
	PrintDeviceConfigurationService
) do (
reg add "HKLM\SYSTEM\CurrentControlSet\Services\%%z" /v "Start" /t REG_DWORD /d "4" /f
)
reg delete "HKCR\SystemFileAssociations\image\shell\print" /f >nul 2>&1
reg delete "HKCR\batfile\shell\print" /f >nul 2>&1
reg delete "HKCR\fonfile\shell\print" /f >nul 2>&1
reg delete "HKCR\cmdfile\shell\print" /f >nul 2>&1
reg delete "HKCR\htmlfile\shell\print" /f >nul 2>&1
reg delete "HKCR\JSEFile\Shell\Print" /f >nul 2>&1
reg delete "HKCR\otffile\shell\print" /f >nul 2>&1
reg delete "HKCR\pfmfile\shell\print" /f >nul 2>&1
reg delete "HKCR\regfile\shell\print" /f >nul 2>&1
reg delete "HKCR\ttcfile\shell\print" /f >nul 2>&1
reg delete "HKCR\ttffile\shell\print" /f >nul 2>&1
reg delete "HKCR\VBEFile\Shell\Print" /f >nul 2>&1
reg delete "HKCR\VBSFile\Shell\Print" /f >nul 2>&1
reg delete "HKCR\WSFFile\Shell\Print" /f >nul 2>&1
DISM.exe /Online /Disable-Feature /FeatureName:"Printing-PrintToPDFServices-Features" /NoRestart >nul 2>&1
DISM.exe /Online /Disable-Feature /FeatureName:"Printing-Foundation-Features" /NoRestart >nul 2>&1
DISM.exe /Online /Disable-Feature /FeatureName:"Printing-Foundation-InternetPrinting-Client" /NoRestart >nul 2>&1