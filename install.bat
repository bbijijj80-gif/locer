@echo off
setlocal enabledelayedexpansion

:: Windows 11 Security Hardener - Installation Script
:: Must be run as Administrator

echo ================================================================
echo   Windows 11 Security Hardener - Installation
echo ================================================================
echo.

:: Check for administrator rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ================================================================
    echo ERROR: Administrator rights required!
    echo ================================================================
    echo Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [1/7] Checking system requirements...

:: Check Python installation
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://python.org and add it to PATH
    pause
    exit /b 1
)
echo [+] Python found.

:: Check source files
if not exist "src\main.py" (
    echo ERROR: src\main.py not found!
    echo Please ensure the src folder contains main.py
    pause
    exit /b 1
)
if not exist "src\requirements.txt" (
    echo ERROR: src\requirements.txt not found!
    pause
    exit /b 1
)
echo [+] Source code found.

echo.
echo [2/7] Installing dependencies (PyInstaller)...
python -m pip install --upgrade pip --quiet
python -m pip install pyinstaller --quiet
if %errorLevel% neq 0 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo [+] PyInstaller installed.

echo.
echo [3/7] Compiling program to EXE...
cd src
python -m PyInstaller --onefile --windowed --name WinSecHardener main.py
if %errorLevel% neq 0 (
    echo ERROR: Compilation failed. Check main.py for syntax errors.
    cd ..
    pause
    exit /b 1
)
cd ..
echo [+] Compilation successful.

echo.
echo [4/7] Creating installation directory...
set INSTALL_DIR=C:\Program Files\WinSecHardener
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"
if %errorLevel% neq 0 (
    echo ERROR: Cannot create installation directory
    pause
    exit /b 1
)
echo [+] Directory created: %INSTALL_DIR%

echo.
echo [5/7] Copying executable...
copy /Y "src\dist\WinSecHardener.exe" "%INSTALL_DIR%\" >nul
if %errorLevel% neq 0 (
    echo ERROR: Cannot copy executable
    pause
    exit /b 1
)
echo [+] Executable copied.

echo.
echo [6/7] Setting ACL permissions (Admin access only)...
:: Set ownership to Administrators group
icacls "%INSTALL_DIR%" /grant Administrators:F /inheritance:r >nul
icacls "%INSTALL_DIR%\WinSecHardener.exe" /grant Administrators:F /inheritance:r >nul
echo [+] ACL permissions set.

echo.
echo [7/7] Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT_PATH=%DESKTOP%\WinSecHardener.lnk

:: Create shortcut using PowerShell
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%INSTALL_DIR%\WinSecHardener.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Windows 11 Security Hardener'; $Shortcut.Save()"
if %errorLevel% neq 0 (
    echo WARNING: Could not create desktop shortcut
) else (
    echo [+] Desktop shortcut created.
)

echo.
echo ================================================================
echo   Installation completed successfully!
echo ================================================================
echo.
echo Program location: %INSTALL_DIR%
echo Desktop shortcut: %DESKTOP%\WinSecHardener.lnk
echo.
echo To run the program, double-click the desktop shortcut
echo or launch WinSecHardener.exe from the installation folder.
echo.
echo NOTE: The program requires administrator rights to run.
echo.
pause
endlocal
