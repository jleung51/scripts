#!/usr/bin/env python3

import argparse
import base64
import json
import os
import requests

from argparse import Namespace
from email.mime.text import MIMEText
from httplib2 import Http

# Gmail API
from apiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

# Configuration

# To create an authentication key, see
# https://msdn.microsoft.com/en-ca/library/ff701720.aspx
bing_maps_auth_key = ""

# Coordinates of the bounding box where traffic incidents are to be monitored
# See https://msdn.microsoft.com/en-us/library/ff701726.aspx
coordinate_southwest = "45.219, -122.325"
coordinate_northeast = "46.610, -122.107"

# See below for the meanings of the severity levels and types.
# Keep only the security levels and types useful to you.
# See https://msdn.microsoft.com/en-ca/library/hh441726.aspx
severity = "1, 2, 3, 4"
type = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"

severity_list = {
    "1" : "Low impact",
    "2" : "Minor",
    "3" : "Moderate",
    "4" : "Serious"
}

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

mail_source_application_name = "Traffic Monitor"
mail_source_email = "gmail_source@email.com"
mail_target_email = "email_target@gmail.com"

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
    for i in incidents:
        coordinates_float = i.get("point").get("coordinates")
        coordinates = '(' + ", ".join(string_list_from(coordinates_float)) + ')'
        print(
                "Alert: " +
                decode_severity(i.get("severity")) + " traffic disruption"
        )

        description = i.get("description")
        description = description[0].lower() + description[1:]
        print(
                decode_type(i.get("type")) + " " +
                description + " Coordinates: " +
                coordinates + "."
        )

        print()

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
    http_auth = get_gmail_credentials().authorize(Http())
    service = build("gmail", "v1", http=http_auth)

    mail = create_message(mail_source_email, mail_target_email, subject, message)
    response = service.users().messages() \
            .send(userId=mail_source_email, body=mail).execute()

    print(json.dumps(response, sort_keys=True, indent=4))

if __name__ == "__main__":
    response = get_traffic_data()
    response_body = response.json()

    alert_for_incidents(response_body)
    alert_to_mail("test_subject", "test_body")
