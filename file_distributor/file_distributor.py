#!/usr/bin/env python3

from contextlib import closing
import configparser
import os

import dropbox
from dropbox.exceptions import ApiError, AuthError

# Custom imports
from logger import Logger
from pcloud_api import PCloudApi
from google_api import GoogleDriveApi

config_filename = "file_distributor.cfg"

def download_dropbox_file(access_token, file_path_dropbox, file_path_local):
    """Logs into a Dropbox account and downloads one specific file.

    Parameters:
    access_token -- String. Dropbox access token. See README.md for
        instructions.
    file_path_dropbox -- String. Path of the file in Dropbox. Begins with a "/".
        E.g. /directory1/directory2/file
    file_path_local -- String. Path to the file locally (relative to the
        location where this script was executed).

    Throws:
    dropbox.exceptions.AuthError -- If authentication fails.
    dropbox.exceptions.ApiError -- If the download fails.
    """
    d = dropbox.Dropbox(access_token)
    try:
        account_info = d.users_get_current_account()
    except AuthError as e:
        Logger.error("Failed to authenticate to Dropbox: " + str(e))
        raise e
    Logger.debug("Account information: " + str(account_info))

    try:
        download_result = d.files_download_to_file(
                file_path_local, file_path_dropbox
        )
    except ApiError as e:
        Logger.error(
                "Failed to download file " + file_path_dropbox +
                " from Dropbox: " + str(e)
        )
        raise e
    Logger.debug(
            "Result of downloading file " + file_path_dropbox + ": " +
            str(download_result)
    )
    Logger.success(
            "Downloaded file " + file_path_dropbox +
            " from Dropbox."
    )

def main():
    config = configparser.ConfigParser()
    config.read(config_filename)

    section_local = "Local"
    file_path_local = config[section_local]["file_path"]

    section_dropbox = "Dropbox"
    dropbox_access_token = config[section_dropbox]["access_token"]
    file_path_dropbox = config[section_dropbox]["file_path"]

    section_pcloud = "pCloud"
    username_pcloud = config[section_pcloud]["username"]
    password_pcloud = config[section_pcloud]["password"]
    dir_path_pcloud = config[section_pcloud]["dir_path"]
    file_name_pcloud = config[section_pcloud]["file_name"]

    section_gdrive = "Google Drive"
    application_name = config[section_gdrive]["application_name"]
    file_name_gdrive = config[section_gdrive]["file_name"]
    parent_dir_id = config[section_gdrive]["parent_dir_id"]

    try:
        download_dropbox_file(
                dropbox_access_token, file_path_dropbox, file_path_local
        )
    except Exception as e:
        Logger.error("File not downloaded from Dropbox: " + str(e))
        raise

    try:
        p = PCloudApi()
        p.login(username_pcloud, password_pcloud)
        p.upload_file(file_path_local, dir_path_pcloud, file_name_pcloud)
        p.logout()
    except Exception as e:
        Logger.error("File not uploaded to pCloud: " + str(e))
        raise

    try:
        g = GoogleDriveApi(application_name)
        # g.list_files()  # Used to find the FileId of a specific directory
        g.upload_file(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), file_path_local
        ), file_name_gdrive, parent_dir_id)
    except Exception as e:
        Logger.error("File not uploaded to Google Drive: " + str(e))

if __name__ == "__main__":
    main()
