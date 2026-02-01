@echo off
REM jcompile-dispatch.cmd - Dispatches Maven compile tasks for fast Java compilation
REM This tool intelligently dispatches compilation tasks across multiple processes

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"

REM Default behavior: clean and compile
set "MAVEN_GOALS=clean compile"
set "MAVEN_OPTS=-T 1C"

:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="--parallel" (
    if not "%~2"=="" (
        set "MAVEN_OPTS=-T %~2"
        shift
    )
    shift
    goto parse_args
)
if /i "%~1"=="--goals" (
    set "MAVEN_GOALS=%~2"
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--threads" (
    set "MAVEN_OPTS=-T %~2"
    shift
    shift
    goto parse_args
)
if /i "%~1"=="-h" goto show_help
if /i "%~1"=="--help" goto show_help

echo Unknown option: %~1
exit /b 1

:show_help
echo Usage: jcompile-dispatch [OPTIONS]
echo.
echo Options:
echo   --parallel [N]    Use parallel compilation (default: 1 thread per core)
echo   --threads N       Use exactly N threads for compilation
echo   --goals GOALS     Custom Maven goals (default: clean compile)
echo   -h, --help        Display this help message
exit /b 0

:end_parse

echo [jcompile-dispatch] Starting dispatch compilation with %MAVEN_OPTS%
echo [jcompile-dispatch] Maven goals: %MAVEN_GOALS%

REM Execute Maven with parallel compilation
call "%SCRIPT_DIR%mvnw.cmd" %MAVEN_OPTS% %MAVEN_GOALS%

if %ERRORLEVEL% equ 0 (
    echo [jcompile-dispatch] Dispatch compilation completed successfully!
) else (
    echo [jcompile-dispatch] Dispatch compilation failed!
    exit /b 1
)

endlocal
