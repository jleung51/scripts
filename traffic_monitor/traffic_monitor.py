#!/usr/bin/env python3

import sys

# Custom modules
from logger import Logger
from bing_api import BingApi
from google_api import GmailApi

# Configuration for traffic incident data:

# Bing Maps authentication key for map data requests.
# Details about the key parameter for the HTTP request:
#   https://msdn.microsoft.com/en-ca/library/ff701720.aspx
#
# Go to the Bing Maps Portal to retrieve your key:
# https://www.bingmapsportal.com/
# Sign in, go to "My Account" -> "My Keys", create a new key, and fill out
# the form. Paste the key into the variable below.
bing_maps_auth_key = ""

# Coordinates of the bounding box where traffic incidents are to be monitored.
# Details about the bounding box:
#   https://msdn.microsoft.com/en-us/library/ff701726.aspx
#
# To find a coordinate, go to Google Maps (yes, I'm aware of the irony):
# https://maps.google.com/
# Right-click on any point and select "What's here?". A small box will appear
# with the coordinate at that location
coordinate_southwest = "45.219, -122.325"
coordinate_northeast = "46.610, -122.107"

# Severity and type of traffic incident.
# Details about severity and type:
#   https://msdn.microsoft.com/en-ca/library/hh441726.aspx
# See the lists below for the interpretation of each level.
#
# Keep only the security levels and types which you want to be notified of,
# and remove the rest.
severity = "1, 2, 3, 4"
incident_type = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"

# Configuration for email notifications:

# Application name from which the email is sent
mail_source_application_name = "Traffic Monitor"

# Gmail account from which your notification emails will be sent.
#
# This should include the "@gmail.com".
mail_source_email = "gmail_source@gmail.com"

# Destination email account to which your notification emails will be sent.
#
# This should include the "@email.com".
mail_target_email = "email_target@email.com"

# Configuration for a report to a Slack channel:

# Change this to True and fill in the following fields if you would like
# to send a report; otherwise, ignore the following fields
report = False
# The API token of the Slackbot (see README:Setup:Reports to a Slack Channel)
# E.g. "xoxb-128312731823-FN3190FHDFK1L1099813UH10"
report_slack_token = ""
# The name of the channel (without a "#")
# E.g. "random"
report_channel = ""
# The name of the Slackbot user which will send the message
# E.g. "Traffic Monitor Slackbot"
report_slackbot_name = ""
# The usernames of Slack users who should be alerted upon a failure
# Each username must begin with a "@"
# E.g. "@jleung51 | @jleung52 | @jleung53"
report_alert_list = ""

# Conditional imports
# Do not modify if you are setting up this script!
if report:
    from slack_messenger import SlackMessenger

def slack_report_message(operation_status, message_text):
    if report:
        s = SlackMessenger(
                report_slack_token, report_channel, report_slackbot_name
        )
        s.operation_report(operation_status, message_text)
        Logger.debug("Slack report sent.")

def slack_notify_users(alert_users, message_text):
    if report:
        s = SlackMessenger(
                report_slack_token, report_channel, report_slackbot_name
        )
        s.notify(alert_users, message_text)
        Logger.debug("Slack alert sent.")

def string_list_from(original_list):
    string_list = []
    for i in original_list:
        string_list.append(str(i))
    return string_list

def send_email_with_incidents(incidents):
    message_text = ""
    for i in incidents:
        description = i.get("description")
        description = description[0].lower() + description[1:]

        message_text += \
                results.get("severity") + " traffic disruption. " + \
                results.get("type") + " " + \
                description + " Coordinates: (" + \
                ", ".join(string_list_from(i.get("coordinates"))) + ")" + \
                ".\n\n"

    message_text += \
            "\nSincerely,\n\n" + \
            "- Your friendly neighborhood Traffic Monitor"

    email_sender = GmailApi(
            mail_source_email, mail_source_application_name
    )
    email_sender.send_email(
            mail_target_email, "Traffic Incident Alert", message_text
    )

    slack_report_message(
            "*SUCCESS*",
            "Traffic incident alert sent to " + mail_target_email + "."
    )

def main():
    b = BingApi(bing_maps_auth_key)
    incidents = b.get_traffic_data_readable(
            coordinate_southwest, coordinate_northeast,
            severity, incident_type)

    if len(incidents) > 0:
        send_email_with_incidents(incidents)
        log_message = "Traffic check completed. " + str(len(incidents)) + \
                " incidents reported."
    else:
        log_message = "Traffic check completed. No incidents reported."

    Logger.success(log_message)
    slack_report_message("*SUCCESS*", log_message)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        slack_report_message(
                report_alert_list, "*ERROR*: Please check the logs."
        )
        raise
