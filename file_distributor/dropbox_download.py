#!/usr/bin/env python3

import time

import configparser
from contextlib import closing

import dropbox
from dropbox.exceptions import ApiError, AuthError

config_filename = "file_distributor.cfg"

class Logger:
    """Outputs formatted log messages."""

    # Change this to True to enable output debug logging for this module.
    print_debug_logs = True

    @classmethod
    def __log(self, log_level, message):
        """Outputs a formatted log message if logging is activated.

        Parameters:
        log_level -- String. Severity of the log message.
        message -- String. Message to be logged.
        """
        if self.print_debug_logs:
            print(
                    "[ " +
                    time.strftime("%Y-%m-%d %H:%M:%S") +
                    " | " +
                    log_level +
                    " ] " +
                    message
            )

    @staticmethod
    def debug(message):
        """Outputs a debug level log message."""
        Logger.__log("DEBUG  ", message)

    @staticmethod
    def success(message):
        """Outputs a success level log message."""
        Logger.__log("SUCCESS", message)

    @staticmethod
    def log_error(message):
        """Outputs a error level log message."""
        Logger.__log("ERROR  ", message)

def download_dropbox_file(access_token, file_path_dropbox, file_path_local):
    """Logs into a Dropbox account and downloads one specific file.

    Parameters:
    access_token -- String. Dropbox access token. See README.md for
        instructions.
    file_path_dropbox -- String. Path of the file in Dropbox. Begins with a "/".
        E.g. /directory1/directory2/file
    file_path_local -- String. Path to the file locally (relative to the
        location where this script was executed).
    """
    d = dropbox.Dropbox(access_token)
    try:
        account_info = d.users_get_current_account()
    except AuthError as e:
        Logger.error("Failed to authenticate to Dropbox: " + str(e))
        exit(1)
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
        exit(1)
    Logger.debug(
            "Result of downloading file " + file_path_dropbox + ": " +
            str(download_result)
    )
    Logger.success(
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
