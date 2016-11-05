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
channel     = ""
# The message which should be sent to the channel
# E.g. "Hello World!"
message     = ""

# SLACK TEAM WHICH A REPORT SHOULD BE SENT TO:

# Change this to True and fill in the following fields if you would like
# to send a report; otherwise, ignore the following fields
report = False
# The API token of the Slackbot (see README:Setup)
# E.g. "xoxb-128312731823-FN3190FHDFK1L1099813UH10"
report_slack_token   = ""
# The name of the channel (without a "#")
# E.g. "random"
report_channel       = ""
# The name of this Slackbot so the report can be identifiable
# E.g. "Weekday Greeter Slackbot"
report_slackbot_name = ""
# The usernames of Slack users who should be alerted upon a failure
# Each username must begin with a "@"
# E.g. "@jleung51 | @jleung52 | @jleung53"
report_alert_list    = ""

def report_result(result):
    if result.get("ok"):
        report_message = "*SUCCESS*\n"
    else:
        report_message = \
                "*ERROR* (Alerting user(s) " + report_alert_list + ")" + '\n'

    SlackClient(report_slack_token).api_call(
        "chat.postMessage",
        channel = "#" + report_channel,
        link_names = 1,
        text = ">>> " + time.strftime("%Y-%m-%d %H:%M:%S") + " | " +
                "Report from _" + report_slackbot_name + '_' + '\n' +
                "Operation status: " + report_message +
                "Response body:\n```\n" +
                json.dumps(result, indent=4, sort_keys=True) + '\n```'
    )

def main():
    result = SlackClient(slack_token).api_call(
        "chat.postMessage",
        channel = "#" + channel,
        text = message
    )
    if report:
        report_result(result)

if __name__ == "__main__":
    main()
