@echo off
echo mitigations on
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v MitigationOptions /f
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v MitigationAuditOptions /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPL /t REG_DWORD /d 1 /f