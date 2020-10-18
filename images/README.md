# Image Editing Scripts

A collection of Python scripts which modify, rename, resize, and otherwise modify images in bulk.

These execute upon all matching images in the folder which the shell is currently in.

## Setup

If Python 3 is not yet installed, then install the relevant packages:
```shell
sudo apt-get install python3 python3-pip
```

Install the PIP dependencies:
```shell
pip3 install -r requirements.txt
```

Run the relevant script.

#### Virtualenv (Optional: Isolated Environment for Python packages)

Install Virtualenv and create an environment named `venv` (or any name you prefer) within your project directory:
```shell
pip3 install virtualenv
cd images/
virtualenv venv
```

Before installing any other packages from the project, activate the virtual environment to isolate your environment for all following commands:
```shell
source venv/bin/activate
```

If on Windows, run the script directly instead:
```
./venv/Scripts/activate
```

Run all Python and PIP commands here.

To deactivate the isolated virtual environment and return to the original environment, either close the console window or run the following command:
```shell
deactivate
```