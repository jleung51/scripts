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

# For the possible values and their explanations, see
# https://msdn.microsoft.com/en-ca/library/hh441726.aspx
severity = "1, 2, 3, 4"
type = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"

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
        print(str(i.get("severity")) + ' ' + str(i.get("type")))
        print(i.get("description"))

        coordinates = i.get("point").get("coordinates")
        print('(' + ", ".join(string_list_from(coordinates)) + ')')
        print()

if __name__ == "__main__":
    response = get_traffic_data()
    response_body = response.json()

    alert_for_incidents(response_body)
