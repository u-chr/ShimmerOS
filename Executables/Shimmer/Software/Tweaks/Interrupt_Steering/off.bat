@echo off
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v InterruptSteeringFlags /t REG_DWORD /d 17 /f
:: not a typo btw
