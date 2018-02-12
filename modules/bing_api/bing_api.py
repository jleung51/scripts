#!/usr/bin/env python3

import requests

from logger import Logger

class BingApi:

    _auth_key = None

    def __init__(self, auth_key):
        """Instantiates a BingAPI object.

        Arguments:
        auth_key -- String. Bing Maps authentication key for map data requests.
            To retrieve your key, go to the Bing Maps Portal: https://www.bingmapsportal.com/
            Sign in, go to "My Account" -> "My Keys", create a new key, and
            fill out the form to retrieve your key.
            See the README for more information.
            Documentation: https://msdn.microsoft.com/en-ca/library/ff701720.aspx
        """
        self._auth_key = auth_key

    @staticmethod
    def __decode_severity(severity):
        # Preset list of incident severity meanings
        severity_list = {
            "1" : "Low impact",
            "2" : "Minor",
            "3" : "Moderate",
            "4" : "Serious"
        }

        string_severity = severity_list[str(severity)]
        if string_severity == None:
            raise ValueError(
                    "An unparseable severity level was found (" +
                    str(severity) + ")"
            )
        return string_severity

    @staticmethod
    def __decode_type(type):
        # Preset list of incident type meanings
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

        string_type = type_list[str(type)]
        if string_type == None:
            raise ValueError(
                    "An unparseable type level was found (" +
                    str(type) + ")"
            )
        return string_type

    def get_traffic_data(self, coordinate_southwest, coordinate_northeast,
            severity=None, type=None):
        """Retrieves traffic data from Bing Maps.

        To find a coordinate, go to Google Maps (yes, I'm aware of the irony),
        right-click on any point, and select "What's here?". A small box will
        appear with the coordinate at that location.

        Arguments:
        coordinate_southwest -- Float. Southwest (bottom-left) coordinate of
            the bounding box where traffic incidents are to be monitored.
            More details: https://msdn.microsoft.com/en-us/library/ff701726.aspx
        coordinate_southwest -- Float. Southwest (bottom-left) coordinate of
            the bounding box where traffic incidents are to be monitored.
            More details: https://msdn.microsoft.com/en-us/library/ff701726.aspx
        severity -- String. Requested severities of the incidents and impacts.
            Example: "1, 2, 3, 4"
            More details: https://msdn.microsoft.com/en-ca/library/hh441726.aspx
        type - String. Requested type of the incidents which occurred.
            Example: "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"
            More details: https://msdn.microsoft.com/en-ca/library/hh441726.aspx

        Returns: Data of all incidents within the bounding box which satisfy
            the requested severity and type.
            Details on the format and contents: https://msdn.microsoft.com/en-us/library/hh441726.aspx
        """
        map_area = ",".join([coordinate_southwest, coordinate_northeast])
        url = "http://dev.virtualearth.net/REST/v1/Traffic/Incidents/" + \
                map_area

        request_params = dict(
            severity = severity,
            type = type,
            key = self._auth_key
        )

        response = requests.get(url, params=request_params)

        log_message = "Bing Maps response: " + str(response.json())
        if response.status_code == requests.codes.ok:
            Logger.debug(log_message)
        else:
            Logger.error(log_message)

        return response

    def get_traffic_data_readable(self, coordinate_southwest,
            coordinate_northeast, severity=None, type=None):
        """Retrieves simplified traffic data from Bing Maps.

        To find a coordinate, go to Google Maps (yes, I'm aware of the irony),
        right-click on any point, and select "What's here?". A small box will
        appear with the coordinate at that location.

        Arguments:
        coordinate_southwest -- Float. Southwest (bottom-left) coordinate of
            the bounding box where traffic incidents are to be monitored.
            More details: https://msdn.microsoft.com/en-us/library/ff701726.aspx
        coordinate_southwest -- Float. Southwest (bottom-left) coordinate of
            the bounding box where traffic incidents are to be monitored.
            More details: https://msdn.microsoft.com/en-us/library/ff701726.aspx
        severity -- String. Requested severities of the incidents and impacts.
            Example: "1, 2, 3, 4"
            More details: https://msdn.microsoft.com/en-ca/library/hh441726.aspx
        type - String. Requested type of the incidents which occurred.
            Example: "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"
            More details: https://msdn.microsoft.com/en-ca/library/hh441726.aspx

        Returns: Data of all incidents within the bounding box which satisfy
            the requested severity and type.
            Format is an array of dicts with the keys:
                coordinates [
                    latitude,
                    longitude
                ]
                description
                severity
                type
        """

        response = self.get_traffic_data(
                coordinate_southwest, coordinate_northeast, severity, type
                )

        if response.status_code != requests.codes.ok:
            raise RuntimeError("HTTP " + str(response.status_code) +
                    "from server.")

        incidents_container = response.json()["resourceSets"]
        if len(incidents_container) is 0:
            incidents = []
        else:
            incidents = incidents_container[0].get("resources")

        incidents_simplified = []
        for i in incidents:
            incidents_simplified.append(dict(
                coordinates = i.get("point").get("coordinates"),
                description = i.get("description"),
                severity = decode_severity(i.get("severity")),
                type = decode_type(i.get("type"))
            ))

        return incidents_simplified
