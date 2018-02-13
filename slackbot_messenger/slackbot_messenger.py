#!/usr/bin/env python3

import json
import sys
import time

from slack_messenger import SlackMessenger

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
    s = SlackMessenger(
            report_slack_token, report_channel, report_slackbot_name
    )

    result_body = "Response body:\n```\n" + \
            json.dumps(result, indent=4, sort_keys=True) + "\n```"

    if result.get("ok"):
        s.operation_report("*SUCCESS*", "Sent message to channel. " + \
                result_body)
    else:
        s.operation_report("*ERROR*", "Failed to send message to " +\
                "Slack channel." + result_body)
        s.notify(report_alert_list, "Internal error, please check the logs.")

def main():
    if len(sys.argv) < 2:
        print("Error: One argument (the message to send) must be provided.")
        sys.exit(1)

    s = SlackMessenger(slack_token, channel, slackbot_name)
    result = s.message(sys.argv[1])

    log_result(result)
    if report:
        report_result(result)

if __name__ == "__main__":
    main()
