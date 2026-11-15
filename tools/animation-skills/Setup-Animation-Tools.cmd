@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-tools.ps1"
if errorlevel 1 (
  echo.
  echo Tool setup did not finish. Read the error above.
  pause
  exit /b 1
)
pause
