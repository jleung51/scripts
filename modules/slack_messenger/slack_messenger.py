#!/usr/bin/env python3
#
# This Python 3 module provides a function to access the Slack API in order
# to send a message to a Slack team.

import json
import time
from slackclient import SlackClient

class Logger:
    """Outputs formatted log messages."""

    # Change this to False to disable all output logging for this module.
    print_logs = True

    @classmethod
    def __log(self, log_level, message):
        """Outputs a formatted log message if logging is activated.
        Parameters:
        log_level -- String. Severity of the log message.
        message -- String. Message to be logged.
        """
        if self.print_logs:
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
    def info(message):
        """Outputs an info level log message."""
        Logger.__log("INFO   ", message)

    @staticmethod
    def success(message):
        """Outputs a success level log message."""
        Logger.__log("SUCCESS", message)

    @staticmethod
    def error(message):
        """Outputs a error level log message."""
        Logger.__log("ERROR  ", message)

class SlackMessenger:

    def __init__(self, slack_token, channel, slackbot_name):
        """Instantiates a Slack messaging object.

        Parameters:
        slack_token -- String. The API token of the Slackbot (see
            README:Setup:Slack Setup)
            E.g. "xoxb-128312731823-FN3190FHDFK1L1099813UH10"
        channel -- String. The name of the channel (without a "#").
            E.g. "random"
        slackbot_name -- String. The name of the Slackbot user which will send
            the message. E.g. "Traffic Monitor Slackbot"
        """

        self.slack_token = slack_token
        self.channel = channel
        self.slackbot_name = slackbot_name

    def message(self, message_text):
        """Sends a message from the Slackbot.

        Parameters:
        message_text -- String. The detailed report message.
            E.g. "Traffic accident on Kingsway and Patterson."

        Does not throw exceptions; outputs any error messages.
        For an example report, see:
        https://github.com/jleung51/scripts/blob/master/modules/slack_messenger/README.md
        """

        try:
            result = SlackClient(self.slack_token).api_call(
                    "chat.postMessage",
                    channel = "#" + self.channel,
                    link_names = 1,
                    username = self.slackbot_name,
                    text = message_text
            )
        except Exception as e:
            Logger.error(
                    "Module slack_messenger | Error: Message not sent. " +
                    "Error message: " + str(e)
            )

        if result.get("ok"):
            Logger.success("Module slack_messenger | Message sent.")
        else:
            Logger.error(
                    "Module slack_messenger | Error: Message not sent. " +
                    "Response body: " + json.dumps(result)
            )

    def notify(self, alert_users, message_text):
        """Sends a notification with tagged user(s) from the Slackbot.

        Parameters:
        alert_users -- String. List of Slack users to be notified.
            E.g. "@jleung51 | @jleung52 | @jleung53"
        message_text -- String. The detailed report message.
            E.g. "Traffic accident on Kingsway and Patterson."

        Does not throw exceptions; outputs any error messages.
        For an example report, see:
        https://github.com/jleung51/scripts/blob/master/modules/slack_messenger/README.md
        """

        self.message("Alerting users " + alert_users + "\n" +
                message_text)

    def operation_report(self, operation_status, message_text):
        """Sends an report with operation status from the Slackbot.

        Parameters:
        operation_status -- String. The general message to summarize the report.
            E.g. "SUCCESS" or "*ERROR*"
        message_text -- String. The detailed report message.
            E.g. "Traffic accident on Kingsway and Patterson."

        Does not throw exceptions; outputs any error messages.
        For an example report, see:
        https://github.com/jleung51/scripts/blob/master/modules/slack_messenger/README.md
        """

        self.message(">>> _" + time.strftime("%Y-%m-%d %H:%M:%S") + '_' +
                '\n' + "Operation status: " + operation_status +
                '\n' + message_text)
