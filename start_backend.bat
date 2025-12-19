@echo off
echo ========================================
echo AI Photo Personalization - Start Backend
echo ========================================
echo.

cd backend\server
call ..\..\env\Scripts\activate.bat

echo Starting Django server on http://localhost:8000
echo.
python manage.py runserver
