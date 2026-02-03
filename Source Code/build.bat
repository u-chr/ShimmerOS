@echo off
rmdir /s /q "dist/Software"
pyinstaller --noconfirm --onedir --windowed --icon="assets\icon2.ico" --add-data "assets;assets" --add-data "TimerResolution;TimerResolution" --add-data "downloads;downloads" --add-data "tools;tools" --add-data "dependencies;dependencies" --hidden-import bs4 --hidden-import win32com --hidden-import psutil main.py --name Shimmer --noconfirm
ren "dist/Shimmer" Software
timeout /t 1 /nobreak >nul
powershell -Command Compress-Archive -Path .\dist\Software -DestinationPath .\dist\Shimmer.zip -Update