@echo off
REM jconfigure.cmd - Configuration tool for JDevtools
REM Sets up and configures the Maven wrapper and project settings

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"

REM Function to check if Java is installed
:check_java
echo [jconfigure] Checking Java installation...
java -version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [jconfigure] ERROR: Java not found. Please install Java 11 or higher.
    exit /b 1
)

for /f "tokens=3" %%g in ('java -version 2^>^&1 ^| findstr /i "version"') do (
    set JAVA_VERSION=%%g
)
echo [jconfigure] Java detected: %JAVA_VERSION%
goto :eof

REM Function to check Maven wrapper
:check_maven_wrapper
if exist "%SCRIPT_DIR%mvnw.cmd" (
    echo [jconfigure] Maven wrapper found
    exit /b 0
) else (
    echo [jconfigure] WARNING: Maven wrapper not found
    exit /b 1
)
goto :eof

REM Function to test Maven wrapper
:test_maven_wrapper
echo [jconfigure] Testing Maven wrapper...
call "%SCRIPT_DIR%mvnw.cmd" --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [jconfigure] Maven wrapper is working correctly
    call "%SCRIPT_DIR%mvnw.cmd" --version
    exit /b 0
) else (
    echo [jconfigure] ERROR: Maven wrapper test failed
    exit /b 1
)
goto :eof

REM Function to show configuration
:show_config
echo.
echo === JDevtools Configuration ===
echo.
echo [jconfigure] Available tools:
echo   - jcompile         : Compile Java code
echo   - jcompile-dispatch: Parallel compilation dispatcher
echo   - jtest            : Run tests
echo   - jconfigure       : Configuration tool (this script)
echo.

if exist "%SCRIPT_DIR%pom.xml" (
    echo [jconfigure] Project configuration (pom.xml) found
) else (
    echo [jconfigure] WARNING: No pom.xml found in current directory
)
echo.
goto :eof

REM Main entry point
set "COMMAND=%~1"

if "%COMMAND%"=="" set "COMMAND=check"

if /i "%COMMAND%"=="check" (
    echo === JDevtools Configuration Tool ===
    echo.
    echo [jconfigure] Running configuration check...
    call :check_java
    if %ERRORLEVEL% neq 0 exit /b 1
    call :check_maven_wrapper
    if %ERRORLEVEL% neq 0 exit /b 1
    call :test_maven_wrapper
    if %ERRORLEVEL% neq 0 exit /b 1
    call :show_config
    echo [jconfigure] Configuration completed successfully!
) else if /i "%COMMAND%"=="test" (
    echo [jconfigure] Testing Maven wrapper...
    call :test_maven_wrapper
) else if /i "%COMMAND%"=="show" (
    call :show_config
) else if /i "%COMMAND%"=="info" (
    call :show_config
) else if /i "%COMMAND%"=="-h" (
    goto show_help
) else if /i "%COMMAND%"=="--help" (
    goto show_help
) else if /i "%COMMAND%"=="help" (
    goto show_help
) else (
    echo [jconfigure] ERROR: Unknown command: %COMMAND%
    echo [jconfigure] Use 'jconfigure --help' for usage information
    exit /b 1
)

goto end

:show_help
echo Usage: jconfigure [COMMAND]
echo.
echo Commands:
echo   check       Check and verify configuration
echo   test        Test Maven wrapper
echo   show        Show current configuration
echo   help        Display this help message
echo.
echo If no command is provided, 'check' is used by default.
exit /b 0

:end
endlocal
