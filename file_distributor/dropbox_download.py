#!/usr/bin/env python3

import time

import configparser
from contextlib import closing

import dropbox
from dropbox.exceptions import ApiError, AuthError

config_filename = "file_distributor.cfg"

# Change this to True to enable output debug logging for this module.
print_debug_logs = True

def log(log_level, message):
    if print_debug_logs:
        print(
                "[ " +
                time.strftime("%Y-%m-%d %H:%M:%S") +
                " | " +
                log_level +
                " ] " +
                message
        )

def log_debug(message):
    log("DEBUG  ", message)

def log_success(message):
    log("SUCCESS", message)

def log_error(message):
    log("ERROR  ", message)

def download_dropbox_file(access_token, file_path_dropbox, file_path_local):
    d = dropbox.Dropbox(access_token)
    try:
        account_info = d.users_get_current_account()
    except AuthError as e:
        log_error("Failed to authenticate to Dropbox: " + str(e))
        exit(1)
    log_debug("Account information: " + str(account_info))

    try:
        download_result = d.files_download_to_file(
                file_path_local, file_path_dropbox
        )
    except ApiError as e:
        log_error(
                "Failed to download file " + file_path_dropbox +
                " from Dropbox: " + str(e)
        )
        exit(1)
    log_debug(
            "Result of downloading file " + file_path_dropbox + ": " +
            str(download_result)
    )
    log_success(
            "Downloaded file " + file_path_dropbox +
            " from Dropbox."
    )

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(config_filename)

    section_local = "Local"
    file_path_local = config[section_local]["file_path"]

    section_dropbox = "Dropbox"
    dropbox_access_token = config[section_dropbox]["access_token"]
    file_path_dropbox = config[section_dropbox]["file_path"]

    download_dropbox_file(
            dropbox_access_token, file_path_dropbox, file_path_local
    )
