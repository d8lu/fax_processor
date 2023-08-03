@echo off
setlocal enabledelayedexpansion
setlocal enableextensions

set "source_directory=.\"
set "target_directory=.\Originals"
set "program_to_run=.\ocrparse.py"

@REM C:\Users\l\anaconda3\python.exe
:loop
if exist "%source_directory%\*.pdf" (
    for %%f in (%source_directory%\*.pdf) do (
            python "%program_to_run%" "%%f"
            move "%%f" "%target_directory%\"
            timeout /t 1 /nobreak >nul
            timeout /t 1 /nobreak >nul
            timeout /t 1 /nobreak >nul
        )
)
timeout /t 1 /nobreak >nul
goto loop