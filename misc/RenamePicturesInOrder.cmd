REM This batch file renames all picture files in the current directory to
REM begin with a unique number, from 01 increasing.
REM
REM A leading 0 is always added.
REM
REM Example input filename:  file.png
REM Example output filename: 04 - file.png

@ECHO off

TITLE "Rename Pictures In Order"

REM Enable variable expansion within for loops
SETLOCAL ENABLEDELAYEDEXPANSION



REM Initialize counter
SET /A NUMBER=1

FOR /R %%i in (*.*) DO (
	REM Extract filename details from FOR loop variables
	SET FILENAME=%%~ni
	SET EXTENSION=%%~xi
	SET ORIGFILENAME=!FILENAME!!EXTENSION!
	
	REM Call subroutine if extension matches (non-case-sensitive)
	IF /I "!EXTENSION!" == ".jpg" CALL :rename !ORIGFILENAME!
	IF /I "!EXTENSION!" == ".jpeg" CALL :rename !ORIGFILENAME!
	IF /I "!EXTENSION!" == ".png" CALL :rename !ORIGFILENAME!
)

EXIT /B



REM Subroutine: rename original_filename
:rename
SET ORIG=%1

REM Add leading 0
IF %NUMBER% LSS 10 (
	SET FORMATNUM=0%NUMBER%
) ELSE (
	SET FORMATNUM=%NUMBER%
)

REM Create resulting filename
SET NEW=%FORMATNUM% - %ORIG%

RENAME %ORIG% "%NEW%"
ECHO %NEW%

REM Increment counter
SET /A NUMBER=NUMBER+1

EXIT /B
