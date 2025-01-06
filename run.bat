@echo off

:: Get the current directory
set "currentDirectory=%cd%"

:: Construct the full path to Main.py
set "mainScriptPath=%currentDirectory%\Code\Main.py"

:: Run the Python script
run "%mainScriptPath%"

