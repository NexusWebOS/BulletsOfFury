@echo off
cd /d "%~dp0"
title Bullets of Fury - Storyroom
python _BUILD_SOURCE\storyboard_server_1024.py
if errorlevel 1 pause
