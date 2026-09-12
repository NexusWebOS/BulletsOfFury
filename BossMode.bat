@echo off
rem ============================================================
rem  BOSS MODE  -  Bullets of Fury boss fight editor
rem
rem  Double-click this. It serves the game folder on localhost and opens the
rem  editor. Closing this window stops the server.
rem
rem  WHY A SERVER AND NOT JUST THE .HTML: bossmode.html fetches the pack's map
rem  JSONs and hosts index.html in an iframe, and a browser blocks both over
rem  file:// - the page would come up with no chrome and a dead engine.
rem
rem  Optional:  BossMode.bat game    the game itself
rem             BossMode.bat debug   the game with debug mode already unlocked
rem ============================================================
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Boss Mode - server

if not exist "bossmode.html" goto nofiles
if not exist "index.html" goto nofiles

rem ---- which page ----
set "PAGE=bossmode.html"
if /i "%~1"=="game"  set "PAGE=index.html"
if /i "%~1"=="debug" set "PAGE=index.html?debug=1"

rem ---- find python (py launcher first, then python on PATH) ----
set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY goto nopython

rem ---- first free port from 8777 up, so a second copy does not fight the first ----
set "PORT="
for %%P in (8777 8778 8779 8780 8781) do (
  if not defined PORT (
    netstat -ano | findstr /r /c:"LISTENING" | findstr /c:":%%P " >nul 2>&1
    if errorlevel 1 set "PORT=%%P"
  )
)
if not defined PORT goto noport

echo.
echo   BOSS MODE
echo   ---------
echo   serving  %CD%
echo   at       http://127.0.0.1:%PORT%/%PAGE%
echo.
echo   The browser opens in a moment. Leave this window open while you work.
echo   Close it (or press Ctrl+C) to stop the server.
echo.

rem The page is opened from a detached shell after a short wait, so the browser
rem never arrives before the server is listening. The server then runs in THIS
rem window, which is what makes closing the window stop it.
start "" /min powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:%PORT%/%PAGE%'"
%PY% -m http.server %PORT% --bind 127.0.0.1
goto :eof

:nofiles
echo.
echo   Cannot find bossmode.html and index.html next to this file.
echo   Keep BossMode.bat in the BulletsOfFury folder.
echo.
pause
exit /b 1

:nopython
echo.
echo   Python was not found - this needs it only as a local file server.
echo   Tried:  py -3     and     python
echo   Install from python.org (tick "Add to PATH"), then run this again.
echo.
pause
exit /b 1

:noport
echo.
echo   Ports 8777-8781 are all busy. Close the other copy of this window,
echo   or edit the port list in this file.
echo.
pause
exit /b 1
