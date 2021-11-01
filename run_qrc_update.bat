@echo off
call .\.venv\Scripts\activate.bat
call pyrcc5 -o project/qrc_resources.py resources/resources.qrc
echo QRC file Updated!
