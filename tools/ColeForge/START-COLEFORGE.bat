@echo off
title ColeForge - Video Smithy
cd /d "%~dp0"

where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo   Node.js was not found on PATH.
  echo   Install it from https://nodejs.org and run this again.
  echo.
  pause
  exit /b 1
)

python -m yt_dlp --version >nul 2>nul
if errorlevel 1 (
  where yt-dlp >nul 2>nul
  if errorlevel 1 (
    echo.
    echo   yt-dlp was not found. Installing it now...
    echo.
    python -m pip install -U yt-dlp
  )
)

set COLEFORGE_OPEN=1
node server.js

echo.
echo   The forge has gone cold.
pause
