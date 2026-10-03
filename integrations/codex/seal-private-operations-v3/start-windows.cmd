@echo off
setlocal
set "ROOT=%~dp0"
cd /d "%ROOT%"
if not exist runtime\.venv\Scripts\python.exe (
  echo Workbench runtime is not installed.
  exit /b 1
)
"%ROOT%runtime\.venv\Scripts\python.exe" "%ROOT%scripts\start_workbench.py" %*
set "RESULT=%ERRORLEVEL%"
if not "%RESULT%"=="0" pause
exit /b %RESULT%
