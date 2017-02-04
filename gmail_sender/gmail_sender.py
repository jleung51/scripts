# This Python 3 module provides a function to access the Gmail API in order
# to send an email from a Gmail account.

import argparse
import base64
import os
import time

from email.mime.text import MIMEText
from httplib2 import Http

# Gmail API
from apiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

# Change this to True to enable output debug logging for this module.
print_debug_logs = False

# Functions:

def log_debug(message):
    log("DEBUG  ", message)

def log_success(message):
    log("SUCCESS", message)

def log_error(message):
    log("ERROR  ", message)

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

def create_message(sender, recipient, subject, message_text):
    message = MIMEText(message_text)
    message["from"] = sender
    message["to"] = recipient
    message["subject"] = subject
    return {"raw":
            base64.urlsafe_b64encode(
                    message.as_string().encode()
            ).decode("utf-8")
    }

class GmailSender:

    def __get_gmail_credentials(self):
        credential_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "generated_credentials.json"
        )
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                    "client_secret.json",
                    "https://www.googleapis.com/auth/gmail.send"
            )
            flow.user_agent = self.application_name

            flags = argparse \
                    .ArgumentParser(parents=[tools.argparser]) \
                    .parse_args()
            flags.noauth_local_webserver = True
            credentials = tools.run_flow(flow, store, flags)
        return credentials

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

        self.__get_gmail_credentials()

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
        log_debug("Mail source:  " + self.source_email)
        log_debug("Mail target:  " + target_email)
        log_debug("Mail subject: " + subject)
        log_debug("Mail message: " + message.replace("\n", "[newline]"))

        http_auth = self.__get_gmail_credentials().authorize(Http())
        service = build("gmail", "v1", http=http_auth)

        mail = create_message(
                self.source_email, target_email,
                subject, message
        )
        response = service.users().messages() \
                .send(userId=self.source_email, body=mail).execute()

        log_debug("Mail sent.")
