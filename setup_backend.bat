@echo off
echo ========================================
echo AI Photo Personalization - Backend Setup
echo ========================================
echo.

cd backend\server

echo Activating virtual environment...
call ..\..\env\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r ..\requirements.txt

echo.
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo ========================================
echo Setup complete!
echo.
echo To start the server, run:
echo   python manage.py runserver
echo ========================================
pause
