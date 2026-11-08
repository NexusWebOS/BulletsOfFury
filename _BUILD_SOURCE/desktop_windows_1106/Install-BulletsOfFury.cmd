@echo off
cd /d "%~dp0"
echo BULLETS OF FURY - VERIFIED WINDOWS SETUP
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-BulletsOfFury.ps1"
if errorlevel 1 (echo Setup could not finish. Read the message above. & pause)
