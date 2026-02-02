@echo off
REM jtest.cmd - Fast Java testing using Maven wrapper
REM Runs Java tests instantly with optimized Maven settings

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"

REM Default Maven goals
set "MAVEN_GOALS=test"
set "MAVEN_OPTS="

:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="--compile" (
    set "MAVEN_GOALS=compile test"
    shift
    goto parse_args
)
if /i "%~1"=="--integration" (
    set "MAVEN_GOALS=verify"
    shift
    goto parse_args
)
if /i "%~1"=="--single" (
    set "MAVEN_OPTS=%MAVEN_OPTS% -Dtest=%~2"
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--method" (
    set "MAVEN_OPTS=%MAVEN_OPTS% -Dtest=%~2"
    shift
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
if /i "%~1"=="--parallel" (
    set "THREAD_COUNT=4"
    if not "%~2"=="" (
        set "THREAD_COUNT=%~2"
        shift
    )
    set "MAVEN_OPTS=%MAVEN_OPTS% -Dparallel=all -DthreadCount=!THREAD_COUNT!"
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
echo Usage: jtest [OPTIONS]
echo.
echo Options:
echo   --compile         Compile before testing
echo   --integration     Run integration tests (verify phase)
echo   --single CLASS    Run a single test class
echo   --method CLASS    Run specific test method
echo   --parallel [N]    Run tests in parallel (default 4 threads)
echo   --offline         Work offline
echo   --debug           Enable debug output
echo   --quiet           Quiet output
echo   -h, --help        Display this help message
exit /b 0

:end_parse

echo [jtest] Starting tests...

REM Execute Maven tests
call "%SCRIPT_DIR%mvnw.cmd" %MAVEN_OPTS% %MAVEN_GOALS%

if %ERRORLEVEL% equ 0 (
    echo [jtest] Tests completed successfully!
) else (
    echo [jtest] Tests failed!
    exit /b 1
)

endlocal
