#!/usr/bin/env python3

from slackclient import SlackClient

import json
import time

# SLACK TEAM WHICH THE MESSAGE SHOULD BE SENT TO:

# The API token of the Slackbot (see README:Setup)
# E.g. "xoxb-128312731823-FN3190FHDFK1L1099813UH10"
slack_token = ""
# The name of the channel (without #)
# E.g. "random"
channel = ""
# The name of the Slackbot user which will send the message
# E.g. "Weekday Greeter Slackbot"
slackbot_name = ""
# The message which should be sent to the channel
# E.g. "Hello World!"
message = ""

# SLACK TEAM WHICH A REPORT SHOULD BE SENT TO:

# Change this to True and fill in the following fields if you would like
# to send a report; otherwise, ignore the following fields
report = False
# The API token of the Slackbot (see README:Setup)
# E.g. "xoxb-128312731823-FN3190FHDFK1L1099813UH10"
report_slack_token = ""
# The name of the channel (without a "#")
# E.g. "random"
report_channel = ""
# The name of the Slackbot user which will send the message
# E.g. "Weekday Greeter Slackbot"
report_slackbot_name = ""
# The usernames of Slack users who should be alerted upon a failure
# Each username must begin with a "@"
# E.g. "@jleung51 | @jleung52 | @jleung53"
report_alert_list = ""

def log_result(result):
    message = "[ " + time.strftime("%Y-%m-%d %H:%M:%S") + " | "
    if result.get("ok"):
        message += "SUCCESS"
    else:
        message += "ERROR  "
    message += " ] Response body: " + json.dumps(result)
    print(message)

def report_result(result):
    if result.get("ok"):
        report_message = "*SUCCESS*"
    else:
        report_message = \
                "*ERROR* (Alerting user(s) " + report_alert_list + ")"

    SlackClient(report_slack_token).api_call(
        "chat.postMessage",
        channel = "#" + report_channel,
        link_names = 1,
        username = report_slackbot_name,
        text = ">>> _" + time.strftime("%Y-%m-%d %H:%M:%S") + '_' +
                '\n' + "Operation status: " + report_message + '\n' +
                "Response body:\n```\n" +
                json.dumps(result, indent=4, sort_keys=True) + "\n```"
    )

def main():
    result = SlackClient(slack_token).api_call(
        "chat.postMessage",
        channel = "#" + channel,
        username = slackbot_name,
        text = message
    )

    log_result(result)
    if report:
        report_result(result)

if __name__ == "__main__":
    main()
