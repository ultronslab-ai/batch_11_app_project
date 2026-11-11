@echo off
title OIL Safety Intelligence App
echo ========================================================
echo   Launching OIL Safety Intelligence Web Application...
echo ========================================================
cd /d "%~dp0"
echo Opening browser at http://localhost:8501 ...
start "" "http://localhost:8501"
"C:\Users\srigo\pypack\Scripts\streamlit.exe" run app.py
pause

