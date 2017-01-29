#!/usr/bin/env python3

import configparser
import hashlib
import requests
import sys
import time

# Change this to True to enable output debug logging for this module.
print_debug_logs = True

# Configuration variables

config = configparser.ConfigParser()
config.read("file_distributor.cfg")

section_local = "Local"
file_path_local = config[section_local]["file_path"]

section_pcloud = "pCloud"
username = config[section_pcloud]["username"]
password = config[section_pcloud]["password"]

def log(log_level, message):
    if print_debug_logs:
        print(
                "[ " +
                time.strftime("%Y-%m-%d %H:%M:%S") +
                " | " +
                log_level +
                " ] " +
                message
        )

def log_debug(message):
    log("DEBUG  ", message)

def log_success(message):
    log("SUCCESS", message)

def log_error(message):
    log("ERROR  ", message)

def sha1_encode(val):
    return hashlib.sha1(val.encode("utf-8")).hexdigest()

class pcloud:
    def __init__(self):
        self.auth_token = None

    def _api_call(self, rest_api, url, params=None,
            response_body_validity_check=None):
        """Makes a REST API call designed for the pCloud service.

        The authentication token will automatically be added to the parameters,
        if it exists.
        """
        if params is None:
            params = dict()
        if response_body_validity_check is None:
            response_body_validity_check = True
        params["auth"] = self.auth_token

        response = requests.get(url=url, params=params)
        response_body = response.json()

        log_debug(rest_api + " status code: " + str(response.status_code))
        log_debug(rest_api + " response body: " + str(response_body))
        if(response.status_code != requests.codes.ok or
                response_body_validity_check(response_body) is False):
            log_error(
                    "Incorrect response (HTTP/1.1 " + str(response.status_code)
                    + ") from " + rest_api + ": " + str(response_body)
            )
            sys.exit(1)

        return response_body

    def _get_digest(self):
        response_body = self._api_call(
                "GET /getdigest", "https://api.pcloud.com/getdigest",
                response_body_validity_check=lambda response_body:
                        response_body is not None and
                        response_body["result"] == 0 and
                        response_body["digest"] is not None
        )
        return response_body["digest"]

    def login(self):
        digest = self._get_digest()
        password_digest = sha1_encode(
                password +
                sha1_encode(username.lower()) +
                digest
        )

        request_params = dict(
                getauth = 1,
                username = username,
                digest = digest,
                passworddigest = password_digest
        )
        response_body = self._api_call(
                "GET /userinfo", "https://api.pcloud.com/userinfo",
                request_params, lambda response_body:
                        response_body is not None and
                        response_body["auth"] is not None
        )

        self.auth_token = response_body["auth"]
        log_debug("Successfully logged in.")

    def logout(self):
        self._api_call(
                "GET /logout", "https://api.pcloud.com/logout",
                response_body_validity_check=lambda response_body:
                        response_body is not None and
                        response_body["auth_deleted"] is not None and
                        response_body["auth_deleted"] is True
        )
        self.auth_token = None
        log_debug("Successfully logged out.")

if __name__ == "__main__":
    p = pcloud()
    p.login()
    p.logout()
