@echo off
REM Change directory to the folder where this script is
cd /d %~dp0

REM Initialize Conda for this shell
call "C:\Users\tanryan\AppData\Local\anaconda3\condabin\conda.bat" activate base

REM Run the Streamlit app
streamlit run Introduction.py

pause
