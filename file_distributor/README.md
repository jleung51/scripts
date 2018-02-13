# File Distributor

Python 3 scripts which download a file from Dropbox and upload it to pCloud and Google Drive.

## Setup

### Custom Modules

Complete the _Setup_ sections of the following modules to set them up in the directory `src/`:

* [Logger](https://github.com/jleung51/scripts/tree/master/modules/logger)
* [Google API](https://github.com/jleung51/scripts/tree/master/modules/google_api)
* [pCloud API](https://github.com/jleung51/scripts/tree/master/modules/pcloud_api)

### Dropbox

Install the pip dependency `dropbox`.

Follow the first few steps in the [Dropbox Developers Tutorial](https://www.dropbox.com/developers/documentation/python#tutorial) to create a Dropbox API application and generate its access token.

### All Scripts

In `file_distributor.cfg`, fill in the variables as described.

### Google Drive: Parent Directory FileId (Optional)

In order to upload a file to a specific directory in Google Drive, the _FileId_ of the parent directory must be provided in the configuration file. If it is not provided, then the file will simply be uploaded to the root directory.

First, manually create the target directory in Google Drive. Set up the scripts as specified above. In `gdrive_upload.py`, comment out the `upload_file()` call and uncomment the `list_files()` call. Execute this script once and the file IDs of all files and directories in your Google Drive will be printed to the console. Find the file ID of the target directory and place it into the configuration file.
