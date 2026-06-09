@echo off
echo ========================================
echo    Library Management System Starting
echo ========================================
echo.

echo Step 1: Creating Virtual Environment...
py -m venv venv

echo Step 2: Activating Virtual Environment...
call venv\Scripts\activate

echo Step 3: Installing Packages...
pip install fastapi==0.111.0 uvicorn==0.29.0 sqlalchemy==2.0.30 python-multipart==0.0.9

echo Step 4: Starting Server...
echo.
echo ========================================
echo   Server running at http://127.0.0.1:8000
echo   API Docs at http://127.0.0.1:8000/docs
echo ========================================
echo.
py -m uvicorn main:app --reload
