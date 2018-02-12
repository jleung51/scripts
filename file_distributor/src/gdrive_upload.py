#!/usr/bin/env python3
#
# This Python 3 script authenticates with Google Drive and uploads a file.
# Authentication details are set in a configuration file. OAuth 2.0 credentials
# are generated from a file named client_secret.json and stored in a file
# named generated_credentials.json. See the README for more details.

import configparser
import os

# Custom imports
from logger import Logger
from google_api import GoogleDriveApi

config_filename = "file_distributor.cfg"

def main():
    config = configparser.ConfigParser()
    config.read(config_filename)

    section_local = "Local"
    file_path_local = config[section_local]["file_path"]

    section_gdrive = "Google Drive"
    application_name = config[section_gdrive]["application_name"]
    file_name_gdrive = config[section_gdrive]["file_name"]
    parent_dir_id = config[section_gdrive]["parent_dir_id"]

    client_secret_file_path = "client_secret.json"

    g = GoogleDriveApi(application_name)

    # g.list_files()  # Can be used to find the FileId of a specific directory

    g.upload_file(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), file_path_local
    ), file_name_gdrive, parent_dir_id)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        Logger.error("File not uploaded to Google Drive: " + str(e))
