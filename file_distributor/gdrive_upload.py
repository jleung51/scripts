#!/usr/bin/env python3

import argparse
import configparser
import httplib2
import os
import sys
import time

# Google Drive API
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

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

class GoogleDrive:
    """Wrapper for the Google Drive API."""

    def __get_credentials(self):
        """Refreshes Google Drive credentials, authorizing if necessary.

        self.__application_name and self.__client_secret_file_path must have
        been set.
        The credentials will be saved to generated_credentials.json.

        Returns OAuth credentials.
        """
        credential_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "generated_credentials.json"
        )
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            scope = "https://www.googleapis.com/auth/drive"
            flow = client.flow_from_clientsecrets(
                    self.__client_secret_file_path, scope
            )
            flow.user_agent = self.__application_name

            flags = argparse \
                    .ArgumentParser(parents=[tools.argparser]) \
                    .parse_args()
            flags.noauth_local_webserver = True
            credentials = tools.run_flow(flow, store, flags)
            Logger.debug("Credentials saved to [" + credential_path + "]")
        return credentials

    def __init__(self, application_name, client_secret_file_path):
        """Initializes and pre-authenticates the Google Drive credentials."""
        self.__application_name = application_name
        self.__client_secret_file_path = client_secret_file_path

        self.__get_credentials()

    def upload_file(self, file_path_local, file_name_gdrive):
        """Uploads a file to a Google Drive account.

        Parameters:
        file_path_local -- String. Absolute path to the file to be uploaded.
        file_name_gdrive -- String. Filename for the uploaded file in
            Google Drive.
        """
        http_auth = self.__get_credentials().authorize(httplib2.Http())
        service = build("drive", "v3", http=http_auth)

        service.files().create(
                media_body=MediaFileUpload(file_path_local),
                body={"name":file_name_gdrive}
        ).execute()

        Logger.debug("File [" + file_path_local + "] uploaded.")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(config_filename)

    section_local = "Local"
    file_path_local = config[section_local]["file_path"]

    section_gdrive = "Google Drive"
    application_name = config[section_gdrive]["application_name"]
    file_name_gdrive = config[section_gdrive]["file_name"]

    client_secret_file_path = "client_secret.json"

    g = GoogleDrive(application_name, client_secret_file_path)
    g.upload_file(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), file_path_local
    ), file_name_gdrive)
