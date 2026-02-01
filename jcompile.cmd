@echo off
REM jcompile.cmd - Fast Java compilation using Maven wrapper
REM Compiles Java code instantly with optimized Maven settings

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"

REM Default Maven goals
set "MAVEN_GOALS=compile"
set "MAVEN_OPTS="

:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="--clean" (
    set "MAVEN_GOALS=clean compile"
    shift
    goto parse_args
)
if /i "%~1"=="--skip-tests" (
    set "MAVEN_OPTS=%MAVEN_OPTS% -DskipTests"
    shift
    goto parse_args
)
if /i "%~1"=="--offline" (
    set "MAVEN_OPTS=%MAVEN_OPTS% -o"
    shift
    goto parse_args
)
if /i "%~1"=="--debug" (
    set "MAVEN_OPTS=%MAVEN_OPTS% -X"
    shift
    goto parse_args
)
if /i "%~1"=="--quiet" (
    set "MAVEN_OPTS=%MAVEN_OPTS% -q"
    shift
    goto parse_args
)
if /i "%~1"=="-h" goto show_help
if /i "%~1"=="--help" goto show_help

REM Pass unknown arguments to Maven
set "MAVEN_OPTS=%MAVEN_OPTS% %~1"
shift
goto parse_args

:show_help
echo Usage: jcompile [OPTIONS]
echo.
echo Options:
echo   --clean           Clean before compiling
echo   --skip-tests      Skip test compilation
echo   --offline         Work offline
echo   --debug           Enable debug output
echo   --quiet           Quiet output
echo   -h, --help        Display this help message
exit /b 0

:end_parse

echo [jcompile] Starting compilation...

REM Execute Maven compilation
call "%SCRIPT_DIR%mvnw.cmd" %MAVEN_OPTS% %MAVEN_GOALS%

if %ERRORLEVEL% equ 0 (
    echo [jcompile] Compilation completed successfully!
) else (
    echo [jcompile] Compilation failed!
    exit /b 1
)

endlocal
