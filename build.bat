@echo off
echo Starting build process...

python -m venv venv
call venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist "app\static\pdfs" mkdir app\static\pdfs
if not exist "output\pdfs" mkdir output\pdfs

python -m compileall app/


echo Build completed successfully!
pause 