# File Distributor

Python 3 scripts which download a file from Dropbox and upload it to pCloud and Google Drive.

## Setup

Install the pip3 dependency `dropbox`.

Follow the first few steps in the [Dropbox Developers Tutorial](https://www.dropbox.com/developers/documentation/python#tutorial) to create a Dropbox API application and generate its access token.

In the configuration variables in `file_distributor.cfg`, fill in the variables as described.

### Google Drive: Parent Directory FileId

In order to upload a file to a specific directory in Google Drive, the FileId of the parent directory must be provided in the configuration file. If it is not provided, then the file will be uploaded to the root directory.

First, manually create the target directory in Google Drive. Set up the scripts as specified above. In `gdrive_upload.py`, comment out the `upload_file()` call and uncomment the `list_files()` call. Execute this script once and the file IDs of all files and directories in your Google Drive will be printed to the console. Find the file ID of the target directory and place it into the configuration file.
