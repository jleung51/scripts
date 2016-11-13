#!/usr/bin/env python3

import argparse
import base64
import json
import os
import requests
import sys
import time

from argparse import Namespace
from email.mime.text import MIMEText
from httplib2 import Http

# Gmail API
from apiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

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
type = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"

# Preset list of incident severity meanings
# Do not modify if you are setting up this script!
severity_list = {
    "1" : "Low impact",
    "2" : "Minor",
    "3" : "Moderate",
    "4" : "Serious"
}

# Preset list of incident type meanings
# Do not modify if you are setting up this script!
type_list = {
    "1" : "Accident",
    "2" : "Congestion",
    "3" : "Disabled vehicle",
    "4" : "Mass transit",
    "5" : "Uncategorized alert",
    "6" : "Uncategorized alert",
    "7" : "Planned event",
    "8" : "Road hazard",
    "9" : "Construction",
    "10" : "General alert",
    "11" : "Weather alert"
}

# Configuration for email notifications:

# Application name from which the email is sent
mail_source_application_name = "Traffic Monitor"

# Gmail account from which your notification emails will be sent.
#
# This should include the "@gmail.com".
mail_source_email = "gmail_source@email.com"

# Destination email account to which your notification emails will be sent.
#
# This should include the "@gmail.com".
mail_target_email = "email_target@gmail.com"

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
    from slackclient import SlackClient

# Functions:

def log_debug(message):
    log("DEBUG  ", message)

def log_success(message):
    log("SUCCESS", message)

def log_error(message):
    log("ERROR  ", message)

def log(log_level, message):
    print(
            "[ " +
            time.strftime("%Y-%m-%d %H:%M:%S") +
            " | " +
            log_level +
            " ] " +
            message
    )

def slack_report_message(operation_status, message_text):
    if report:
        SlackClient(report_slack_token).api_call(
                "chat.postMessage",
                channel = "#" + report_channel,
                link_names = 1,
                username = report_slackbot_name,
                text = ">>> _" + time.strftime("%Y-%m-%d %H:%M:%S") + '_' +
                        '\n' + "Operation status: " + operation_status + '\n' +
                        message_text
        )
        log_debug("Slack report sent.")

def decode_severity(severity):
    string_severity = severity_list[str(severity)]
    if string_severity == None:
        raise ValueError(
                "An unparseable severity level was found (" +
                str(severity) + ")"
        )
    return string_severity

def decode_type(type):
    string_type = type_list[str(type)]
    if string_type == None:
        raise ValueError(
                "An unparseable type level was found (" +
                str(type) + ")"
        )
    return string_type

def string_list_from(original_list):
    string_list = []
    for i in original_list:
        string_list.append(str(i))
    return string_list

def get_traffic_data():
    map_area = ",".join([coordinate_southwest, coordinate_northeast])
    url = "http://dev.virtualearth.net/REST/v1/Traffic/Incidents/" + map_area

    req_params = dict(
        severity = severity,
        type = type,
        key = bing_maps_auth_key
    )

    return requests.get(url, params=req_params)

def alert_for_incidents(response_body):
    incidents_container = response_body["resourceSets"]
    if len(incidents_container) is 0:
        return
    incidents = incidents_container[0].get("resources")

    message_text = ""
    for i in incidents:
        coordinates_float = i.get("point").get("coordinates")
        coordinates = '(' + ", ".join(string_list_from(coordinates_float)) + ')'
        description = i.get("description")
        description = description[0].lower() + description[1:]

        message_text += \
                decode_severity(i.get("severity")) + " traffic disruption. " + \
                decode_type(i.get("type")) + " " + \
                description + " Coordinates: " + \
                coordinates + "." + \
                '\n\n'

    if message_text:
        message_text += \
                "\nSincerely,\n\n" + \
                "- Your friendly neighborhood Traffic Monitor"
        alert_to_mail("Traffic Incident Alert", message_text)
        slack_report_message(
                "*SUCCESS*",
                "Traffic incident alert sent to " + mail_target_email + "."
        )
    else:
        slack_report_message("*SUCCESS*", "No incidents found.")

def get_gmail_credentials():
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
        flow.user_agent = mail_source_application_name

        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        flags.noauth_local_webserver = True
        credentials = tools.run_flow(flow, store, flags)
    return credentials

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

def alert_to_mail(subject, message):
    log_debug("Mail source:  " + mail_source_email)
    log_debug("Mail target:  " + mail_target_email)
    log_debug("Mail subject: " + subject)
    log_debug("Mail message: " + message.replace("\n", "[newline]"))

    http_auth = get_gmail_credentials().authorize(Http())
    service = build("gmail", "v1", http=http_auth)

    mail = create_message(mail_source_email, mail_target_email, subject, message)
    response = service.users().messages() \
            .send(userId=mail_source_email, body=mail).execute()

    log_debug("Mail sent.")

def main():
    response = get_traffic_data()
    response_body = response.json()

    log_message = "Bing Maps response: " + str(response_body)
    if response.status_code == requests.codes.ok:
        log_debug(log_message)
    else:
        log_error(log_message)
        sys.exit(1)

    alert_for_incidents(response_body)

    log_success("Operation completed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        slack_report_message(
                "*ERROR* (Alerting user(s) " + report_alert_list + ")",
                "Internal Error. Please check the logs."
        )
        raise
