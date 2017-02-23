@ECHO OFF
SETLOCAL ENABLEEXTENSIONS

REM This Windows batch script removes empty lines from a text file.
ECHO [Script executed at %DATE%-%TIME%] Removing empty lines from file %FILEPATH%

SET FILEPATH=%1

IF "%FILEPATH%"=="" (
    ECHO Error: An absolute file path must be provided as the argument.
    EXIT /B 1
)
IF NOT EXIST "%FILEPATH%" (
    ECHO Error: The given file does not exist.
    EXIT /B 1
)

COPY %FILEPATH% %FILEPATH%.tmp
FINDSTR "." %FILEPATH%.tmp > %FILEPATH%
DEL %FILEPATH%.tmp

EXIT
