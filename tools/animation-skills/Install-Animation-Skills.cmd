@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
if errorlevel 1 (
  echo.
  echo Installation did not finish. Read the error above.
  pause
  exit /b 1
)
echo.
echo Open a new Codex chat to load the installed skills.
pause
