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

def get_traffic_data():
    map_area = ",".join([coordinate_southwest, coordinate_northeast])
    url = "http://dev.virtualearth.net/REST/v1/Traffic/Incidents/" + map_area

    req_params = {}
    req_params["severity"] = severity
    req_params["type"] = type
    req_params["key"] = bing_maps_auth_key

    return requests.get(url, params=req_params)

if __name__ == "__main__":

    response = get_traffic_data()
    response_body = response.json()

    print(json.dumps(response_body, sort_keys=True, indent=4))
