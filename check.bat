@echo off
setlocal

set "developer_username=Armaan"
set "correct_password=coder++"

set /p "input_username=Enter admin username: "
set /p "input_password=Enter admin password: "

set "base_path=%USERPROFILE%\Desktop\Project"

cd ..
set "parent_directory=%CD%"
echo %parent_directory%


if /I "%input_username%"=="%developer_username%" (
    if "%input_password%"=="%correct_password%" (
        echo Access granted. Opening folder.
        start "" "%base_path%"
        call "%base_path%\run.bat"
    ) else (
        echo Incorrect password. You do not have access to the code.
        call "%base_path%\run.bat"
        pause
        exit
    )
) else (
    echo Incorrect username. You do not have access to the code.
    call "%base_path%\run.bat"
    pause
    exit
)

endlocal
