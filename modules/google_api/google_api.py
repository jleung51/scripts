# This Python 3 module provides classes to access the Google API.

import argparse
import os

from httplib2 import Http

# Google API
from apiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

# Gmail
import base64
from email.mime.text import MIMEText

# Google Drive
import json
from apiclient.http import MediaFileUpload

# Custom modules
from logger import Logger

class _GoogleApi:
    """Template for a wrapper class for the Google API.

    To use, extend this class in the same file.
    """

    _scope = ""

    def _get_credentials(self):
        """Refreshes Google access credentials, authorizing if necessary.

        self._scope must have been set in the subclass.

        Requires a client_secret.json file in the same directory. See README
        for instructions to create it.
        The credentials will be saved to generated_credentials.json.

        Arguments:
        scope -- String. Google Authentication scope which allows for a specific
            area of access.
            https://developers.google.com/identity/protocols/googlescopes
        Returns: OAuth credentials.
        """
        credential_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "generated_credentials.json"
        )
        store = Storage(credential_path)

        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                "client_secret.json", self._scope
            )
            flow.user_agent = self.application_name

            flags = argparse \
                    .ArgumentParser(parents=[tools.argparser]) \
                    .parse_args()
            flags.noauth_local_webserver = True
            credentials = tools.run_flow(flow, store, flags)

            Logger.debug(
                    "Google Drive credentials saved to [" +
                    credential_path + "]"
            )

        return credentials

class GmailApi(_GoogleApi):
    """Wrapper for the Gmail API."""

    _scope = "https://www.googleapis.com/auth/gmail.send"

    def _create_message(self, sender, recipient, subject, message_text):
        message = MIMEText(message_text)
        message["from"] = sender
        message["to"] = recipient
        message["subject"] = subject
        return {"raw":
                base64.urlsafe_b64encode(
                        message.as_string().encode()
                ).decode("utf-8")
        }

    def __init__(self, source_email, application_name=None):
        """Instantiates a GmailApi object and refreshes its credentials.

        Parameters:
        source_email -- String. Gmail account from which your emails
            will be sent. This should include the "@gmail.com".
            E.g. "gmail_source@email.com"
        application_name -- String. Application name from which the
            email is sent. Internal to the Google API.
        """
        if application_name is None:
            application_name = "Mail Sender"

        self.source_email = source_email
        self.application_name = application_name

        self._get_credentials()

    def send_email(self, target_email, subject, message):
        """Sends an email to the specific email address.

        Parameters:
        target_email -- String. Destination email account to which your email
            will be sent. This should include the "@____.com".
            E.g. "john_smith@email.com"
        subject -- String. Text describing the subject of the email.
        message -- String. Message body of the email. Use newlines ("\n")
            for line breaks.
        """
        Logger.debug("Mail source:  " + self.source_email)
        Logger.debug("Mail target:  " + target_email)
        Logger.debug("Mail subject: " + subject)
        Logger.debug("Mail message: " + message.replace("\n", "[newline]"))

        http_auth = self._get_credentials().authorize(Http())
        service = build("gmail", "v1", http=http_auth)

        mail = self._create_message(
                self.source_email, target_email,
                subject, message
        )
        response = service.users().messages() \
                .send(userId=self.source_email, body=mail).execute()

        Logger.debug("Mail sent.")

class GoogleDriveApi(_GoogleApi):
    """Wrapper for the Google Drive API (v3)."""

    _scope = "https://www.googleapis.com/auth/drive"

    def __init__(self, application_name=None):
        """Instantiates a GmailApi object and refreshes its credentials.

        Parameters:
        source_email -- String. Gmail account from which your emails
            will be sent. This should include the "@gmail.com".
            E.g. "gmail_source@email.com"
        application_name -- String. Application name from which the
            email is sent. Internal to the Google API.
        """
        if application_name is None:
            application_name = "Google Drive Accesser"

        self.application_name = application_name

        http_auth = self._get_credentials().authorize(Http())
        self.__service = build("drive", "v3", http=http_auth)

    def get_file_list(self):
        """Retrieves the data of all files  and dirs in the Google Drive.

        Reference: https://developers.google.com/drive/v3/reference/files/list
        """
        file_list = []

        pageToken = ""
        while(pageToken is not None):
            file_obj = self.__service.files()\
                    .list(pageToken=pageToken).execute()
            file_list.extend(file_obj.get("files"))
            pageToken = file_obj.get("nextPageToken")

        Logger.debug("File and directory details:")
        for file in file_list:
            Logger.debug("  " + json.dumps(file))

        return file_list

    def upload_file(self, file_path_local,
            file_name_gdrive, parent_dir_id=None):
        """Uploads a file to a Google Drive account.

        Parameters:
        file_path_local -- String. Absolute path to the file to be uploaded.
        file_name_gdrive -- String. Filename for the uploaded file in
            Google Drive.
        parent_dir_id -- String (optional). File ID for the parent directory
            of the uploaded file. See README.md for instructions.
        """
        body = {"name": file_name_gdrive}
        if parent_dir_id is not None:
            body["parents"] = [parent_dir_id]

        self.__service.files().create(
                body=body,
                media_body=MediaFileUpload(file_path_local),
        ).execute()

        Logger.debug("File [" + file_path_local + "] uploaded to Google Drive.")
