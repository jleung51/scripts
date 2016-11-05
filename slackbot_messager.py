#!/usr/bin/env python3

from slackclient import SlackClient

import json
import time

slack_token = ""
channel     = ""
message     = ""

report_slack_token   = ""
report_channel       = ""
report_slackbot_name = ""
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
    report_result(result)

if __name__ == "__main__":
    main()
