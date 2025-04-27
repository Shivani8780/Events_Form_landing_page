@echo off
REM Start Serveo tunnel and Django server with environment variable set

REM Start Serveo tunnel on port 8000 and save URL to a file
start cmd /k "ssh -R 80:localhost:8000 serveo.net > serveo_url.txt"

REM Wait for Serveo to start and get URL
timeout /t 5

REM Read the Serveo URL from the file
for /f "tokens=*" %%a in (serveo_url.txt) do (
    echo %%a | findstr /r /c:"https://.*\.serveo\.net" >nul
    if not errorlevel 1 (
        set SERVEO_URL=%%a
        goto :found
    )
)
:found

REM Extract the URL from the line
for /f "tokens=1" %%b in ("%SERVEO_URL%") do set PUBLIC_BASE_URL=%%b

echo Serveo URL detected: %PUBLIC_BASE_URL%

REM Set environment variable for this session
set PUBLIC_BASE_URL=%PUBLIC_BASE_URL%

REM Start Django server with environment variable
python manage.py runserver
