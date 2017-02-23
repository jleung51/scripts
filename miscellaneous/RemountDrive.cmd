@ECHO OFF
SETLOCAL ENABLEEXTENSIONS

REM This Windows batch file mounts a virtual hard drive, creates a file in it, removes the file, and then unmounts the hard drive.
REM
REM Setup:
REM   1.  Open _Disk Management_ through the Start menu
REM   2.  Navigate to _Action_ and select _Create VHD_
REM   3.  Select the location for the virtual hard drive file and set the size to 10MB or greater
REM   4.  Set the configuration variable VIRTUALDRIVE to the path of the virtual hard drive file created in the previous step
REM   5.  Right click the new disk, select _Initialize Disk_, and click _OK_
REM   6.  Right-click on the unallocated space in the new disk and select _New Simple Volume_
REM   7.  Follow the wizard; in the screen _Assign Drive Letter or Path_, choose not to assign them
REM   8.  Open a new command line window and type MOUNTVOL
REM   9.  From the output, copy the volume name of your newly created hard drive (e.g. \\?\Volume{2f823551-0df2-11e6-96ba-806e6f6e6963}) into the configuration variable VOLUME below
REM   10. Assign the volume an unused drive letter in the configuration variable DRIVE below
REM   11. Execute this script

ECHO [Script executed at %DATE%-%TIME%]

REM VirtualDrive: Configuration variable
REM VirtualDrive: Path of the virtual hard drive file created using _Disk Management_ during setup
REM VirtualDrive: E.g. C:\drive\virtual_hard_drive.vhd
SET VIRTUALDRIVE=

REM Volume: Configuration variable
REM Volume: Unique identifier for the volume; open command prompt and type MOUNTVOL to find the volume name
REM Volume: E.g. \\?\Volume{2f823551-0df2-11e6-96ba-806e6f6e6963}\
SET VOLUME=

REM Drive: Configuration variable
REM Drive: Letter to denote the mount point
REM Drive: E.g. D
SET DRIVE=

REM Flesh out configuration variables
SET DRIVE=%DRIVE%:

REM Attach virtual hard drive
CALL :AttachDrive %VIRTUALDRIVE% RETVAL
IF %RETVAL% neq 0 (
  ECHO Error: Virtual hard drive %VIRTUALDRIVE% could not be attached.
  EXIT /B %RETVAL%
)

REM Check for empty drive letter
CALL :CheckUnmounted %DRIVE% RETVAL
IF %RETVAL% neq 0 (
  ECHO Error: Drive %DRIVE% is already in use.
  EXIT /B %RETVAL%
)

REM Mount volume to the drive and check status of drive
MOUNTVOL %DRIVE% %VOLUME%
CALL :CheckMounted %DRIVE% RETVAL
IF %RETVAL% neq 0 (
  ECHO Error: Failed to mount volume on drive %DRIVE%. Errorlevel %RETVAL%.
  EXIT /B %RETVAL%
)

REM Add and remove file
ECHO This file can be deleted.> %DRIVE%\tmp.txt
DEL %DRIVE%\tmp.txt

REM Unmount volume from the drive and check status of drive
MOUNTVOL %DRIVE% /P
CALL :CheckUnmounted %DRIVE% RETVAL
IF %RETVAL% neq 0 (
  ECHO Error: Failed to unmount volume from drive %DRIVE% . Errorlevel %RETVAL%.
  EXIT /B %RETVAL%
)

REM Detach virtual hard drive
CALL :DetachDrive %VIRTUALDRIVE% RETVAL
IF %RETVAL% neq 0 (
  ECHO Error: Virtual hard drive %VIRTUALDRIVE% could not be detached.
  EXIT /B %RETVAL%
)

ECHO [Script finished at %DATE%-%TIME%]
EXIT /B 0

REM This function attaches a virtual hard drive.
REM
REM Parameters:
REM   1. Path to the virtual hard drive file (e.g. C:\drive\virtual_hard_drive.vhd)
REM   2. Return value
REM     Equals 0 if the drive is successfully attached
REM     Equals 1 in any other case
:AttachDrive
SET TEMPSCRIPT=%TEMP%\diskpart-script-%RANDOM%
TYPE NUL > %TEMPSCRIPT%
ECHO SELECT VDISK FILE=%~1 >> %TEMPSCRIPT%
ECHO ATTACH VDISK >> %TEMPSCRIPT%

SET EXITCODE=0
DISKPART /s %TEMPSCRIPT% > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
  SET EXITCODE=1
)

DEL %TEMPSCRIPT%
SET %~2=%EXITCODE%
EXIT /B %EXITCODE%

REM This function detaches a virtual hard drive.
REM
REM Parameters:
REM   1. Path to the virtual hard drive file (e.g. C:\drive\virtual_hard_drive.vhd)
REM   2. Return value
REM     Equals 0 if the drive is successfully detached
REM     Equals 1 in any other case
:DetachDrive
SET TEMPSCRIPT=%TEMP%\diskpart-script-%RANDOM%
TYPE NUL > %TEMPSCRIPT%
ECHO SELECT VDISK FILE=%~1 >> %TEMPSCRIPT%
ECHO DETACH VDISK >> %TEMPSCRIPT%

SET EXITCODE=0
DISKPART /s %TEMPSCRIPT% > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
  SET EXITCODE=1
)

DEL %TEMPSCRIPT%
SET %~2=%EXITCODE%
EXIT /B %EXITCODE%

REM This function checks that a certain drive is mounted.
REM
REM Parameters:
REM   1: Drive letter with trailing colon (e.g. C:)
REM   2: Return value
REM     Equals 0 if the drive is mounted
REM     Equals non-zero in any other case
:CheckMounted
SET DRIVE=%~1
MOUNTVOL %DRIVE% /L > NUL 2>&1
SET %~2=%EXITCODE%
EXIT /B %EXITCODE%

REM This function checks that a certain drive is unmounted.
REM
REM Parameters:
REM   1: Drive letter with trailing colon (e.g. C:)
REM   2: Return value
REM     Equals 0 if the drive is not mounted
REM     Equals 1 in any other case
:CheckUnmounted
SET DRIVE=%~1
SET EXITCODE=1
MOUNTVOL %DRIVE% /L > NUL 2>&1
IF %ERRORLEVEL% EQU 1 (  REM Must be immediately after MOUNTVOL
  SET EXITCODE=0
)
SET %~2=%EXITCODE%
EXIT /B %EXITCODE%
