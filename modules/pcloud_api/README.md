# PCloud Api

Python 3 module which provides a wrapper for the [pCloud APIs](https://docs.pcloud.com/).

## Setup

Setup the [Logger](https://github.com/jleung51/scripts/tree/master/modules/logger) module in this directory.

## Usage

Add the `pcloud_api.py` module and its dependencies to the directory of the Python program. Import the module in your program:
```
from pcloud_api import PCloudApi
```

Create an object to access the API:
```
p = PCloudApi()

Login, upload a file, and log out:
```
p.login(username_pcloud, password_pcloud)
p.upload_file(file_path_local, dir_path_pcloud, file_name_pcloud)
p.logout()
```

For detailed information on the parameters and usage, see the documentation in the class.
