@echo off
REM ============================================================
REM  BULLETS OF DEBUG!  - the editor for everything that is not a boss.
REM  Sibling of BossMode.bat: same server, different front page.
REM  Must be served over http - the editor fetch()es its atlas maps,
REM  and file:// blocks that.
REM ============================================================
setlocal
set PY=
for %%P in (py python) do (
  if not defined PY (
    %%P -c "import sys" >nul 2>&1 && set PY=%%P
  )
)
if not defined PY (
  echo Could not find Python. Install it, or serve the folder yourself and open bulletsofdebug.html
  pause
  exit /b 1
)
cd /d "%~dp0"
set PORT=
for %%N in (8787 8788 8789 8790 8791) do (
  if not defined PORT (
    %PY% -c "import socket,sys;s=socket.socket();r=s.connect_ex(('127.0.0.1',%%N));s.close();sys.exit(0 if r else 1)" >nul 2>&1 && set PORT=%%N
  )
)
if not defined PORT set PORT=8787
echo Serving %CD% on http://127.0.0.1:%PORT%
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:%PORT%/bulletsofdebug.html'"
%PY% -m http.server %PORT% --bind 127.0.0.1
