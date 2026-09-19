@echo off
rem Startet die gebaute Exe im Selbsttest-Modus und zeigt die Zeile (PY_TOOL_DESIGN.md 7.6).
set "TW1HUB_SELFTEST=%TEMP%\hub_selftest.txt"
del "%TW1HUB_SELFTEST%" 2>nul
start "" /wait "%~dp0dist\TW1_Modding_Hub.exe"
timeout /t 3 >nul
type "%TW1HUB_SELFTEST%"
