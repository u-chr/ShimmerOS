@echo off
reg add "HKCU\Software\Microsoft\Clipboard" /v EnableClipboardHistory /t REG_DWORD /d 1 /f
reg add "HKCU\Software\Microsoft\Clipboard" /v AllowClipboardHistory /t REG_DWORD /d 1 /f
sc config cbdhsvc start= auto