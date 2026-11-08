@echo off
setlocal
cd /d "%~dp0"
title Bullets of Fury - Official Tester Build
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0PLAY_LOCAL.ps1"
if errorlevel 1 (
 echo The game server could not start. Please keep this error for Mike.
 pause
)
