REM This Windows batch script removes empty lines from a text file.

IF "%1"=="" (
    ECHO Error: An absolute file path must be provided as the argument.
    EXIT /B 1
)

REM [%DATE%-%TIME%] Removing empty lines from file %1

COPY %1 %1.tmp
FINDSTR "." %1.tmp > %1
DEL %1.tmp
