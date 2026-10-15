@echo off
REM Local fullscreen launch helper for Bullets of Fury Overdrive.
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title Bullets of Fury - Overdrive Ground Operations

if not exist "expansion/topdown/index.html" goto nofiles

set "PYEXE="
set "PYARGS="
py -3 -c "import sys" >nul 2>&1
if not errorlevel 1 (
  set "PYEXE=py"
  set "PYARGS=-3"
)
if not defined PYEXE (
  python -c "import sys" >nul 2>&1
  if not errorlevel 1 set "PYEXE=python"
)
if not defined PYEXE goto nopython

set "PORT="
for %%P in (8765 8766 8767 8768 8769 8770 8771 8772) do (
  if not defined PORT (
    netstat -ano | findstr /r /c:"LISTENING" | findstr /c:":%%P " >nul 2>&1
    if errorlevel 1 set "PORT=%%P"
  )
)
if not defined PORT goto noport

echo.
echo   BULLETS OF FURY - OVERDRIVE GROUND OPERATIONS
echo   ---------------------------------
echo   Music priority mix: ON
echo   Serving: %CD%
echo   Fullscreen launch: ON
echo   Game:    http://127.0.0.1:%PORT%/expansion/topdown/index.html?fullscreen=1
echo.
echo   Leave this window open while playing.
echo   Close it or press Ctrl+C to stop the server.
echo.

start "" /min powershell -NoProfile -WindowStyle Hidden -Command "& %PYEXE% %PYARGS% 'expansion/topdown/_research/launch_overdrive_1011.py' %PORT%"
%PYEXE% %PYARGS% -m http.server %PORT% --bind 127.0.0.1
exit /b %errorlevel%

:nofiles
echo ERROR: expansion/topdown/index.html was not found beside this launcher.
pause
exit /b 1

:nopython
echo ERROR: Python 3 is required for the local full-sound server.
echo Install Python 3, enable Add Python to PATH, then run this file again.
pause
exit /b 1

:noport
echo ERROR: Local ports 8765 through 8772 are busy.
echo Close another local server and run this launcher again.
pause
exit /b 1
