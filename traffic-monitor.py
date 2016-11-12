#!/usr/bin/env python3

import json
import requests

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

if __name__ == "__main__":
    response = get_traffic_data()
    response_body = response.json()

    alert_for_incidents(response_body)
