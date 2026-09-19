@echo off
rem Baut den TW1 Modding Hub als eine Exe (PyInstaller, onefile, ohne Konsole).
rem Ergebnis: %~dp0dist\TW1_Modding_Hub.exe
setlocal
pushd "%~dp0"
py -3.13 -m PyInstaller --noconfirm --onefile --windowed ^
  --name "TW1_Modding_Hub" --icon "%~dp0modding_hub.ico" ^
  --add-data "%~dp0modding_hub.ico;." --add-data "%~dp0untested.json;." ^
  --add-data "%~dp0guides;guides" ^
  --hidden-import theme --hidden-import guidebook --hidden-import updater --hidden-import version ^
  --hidden-import data --hidden-import foxfeedback --hidden-import foxfeedback_ui ^
  --distpath "%~dp0dist" --workpath "%TEMP%\hub_build" --specpath "%TEMP%\hub_build" modding_hub.py
set rc=%errorlevel%
popd
if %rc% neq 0 (echo BUILD FEHLGESCHLAGEN & exit /b %rc%)
echo BUILD OK: %~dp0dist\TW1_Modding_Hub.exe
