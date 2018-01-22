#!/usr/bin/env python3
#
# This Python 3 module provides a function to access the Slack API in order
# to send a log or operation report to a Slack team.

import time
from slackclient import SlackClient

# Change this to True to enable output debug logging for this module.
print_debug_logs = False

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

class SlackLogger:

    def __init__(self, slack_token, channel, slackbot_name):
        """Instantiates an Slack logging object.

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

    def report(self, operation_status, message_text):
        """Sends a report to the Slackbot configured during instantiation.

        Parameters:
        operation_status -- String. The general message to summarize the report.
            E.g. "SUCCESS" or "*ERROR*"
        message_text -- String. The detailed report message.
            E.g. "Traffic accident on Kingsway and Patterson."

        Does not throw exceptions; outputs any error messages.
        For an example report, see:
        https://github.com/jleung51/scripts/blob/master/slack_logger/README.md
        """

        try:
            SlackClient(self.slack_token).api_call(
                    "chat.postMessage",
                    channel = "#" + self.channel,
                    link_names = 1,
                    username = self.slackbot_name,
                    text = ">>> _" + time.strftime("%Y-%m-%d %H:%M:%S") + '_' +
                            '\n' + "Operation status: " + operation_status +
                            '\n' + message_text
            )
            log_success("Module slack_logger | Slack report sent.")
        except Exception as e:
            log_error("Module slack_logger | Error: Slack report not sent.")
            raise

