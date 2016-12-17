REM This Windows batch script logs into Perforce and updates a file named `last_updated` in the depot with the current date and timestamp.
REM This can be set up to be executed upon startup/login to avoid expiration of access permissions upon a lack of recent Perforce updates.

SET P4PORT=
SET P4CLIENT=
SET P4USER=
SET P4PASSWD=
SET DIR=

SET FILEPATH=%DIR%\last_updated

p4 login -s
p4 info
p4 sync -q

REM If the file does not exist, ADD will be successful; if the file does exist, EDIT will be successful
p4 add %FILEPATH%
p4 edit %FILEPATH%

ECHO %DATE%-%TIME% > %FILEPATH%
p4 submit -d "Update" %FILEPATH%

p4 logout
