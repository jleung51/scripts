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

def get_digest():
    response = requests.get("https://api.pcloud.com/getdigest")
    response_body = response.json()

    log_debug("GET /getdigest status code: " + str(response.status_code))
    log_debug("GET /getdigest response body: " + str(response_body))
    if(response.status_code != requests.codes.ok or
            response_body is None or
            response_body["result"] != 0 or
            response_body["digest"] is None):
        log_error(
                "Incorrect response (HTTP/1.1 " + response.status_code +
                ") from GET /getdigest: " + str(response_body)
        )
        sys.exit(1)

    return response_body["digest"]

def sha1_encode(val):
    return hashlib.sha1(val.encode("utf-8")).hexdigest()

def get_auth_token():
    digest = get_digest()

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

    response = requests.get(
            "https://api.pcloud.com/userinfo", params=request_params
    )
    response_body = response.json()

    log_debug("GET /userinfo status code: " + str(response.status_code))
    log_debug("GET /userinfo response body: " + str(response_body))
    if(response.status_code != requests.codes.ok or
            response_body is None or
            response_body["auth"] is None):
        log_error(
                "Incorrect response (HTTP/1.1 " + response.status_code +
                ") from GET /userinfo: " + str(response_body)
        )
        sys.exit(1)

    log_debug("Authentication token: " + response_body["auth"])
    return response_body["auth"]

def logout(auth_token):
    request_params = dict(auth = auth_token)
    response = requests.get(
            "https://api.pcloud.com/logout", params=request_params
    )
    response_body = response.json()

    log_debug("GET /logout status code: " + str(response.status_code))
    log_debug("GET /logout response body: " + str(response_body))
    if(response.status_code != requests.codes.ok or
            response_body is None or
            response_body["auth_deleted"] is None or
            response_body["auth_deleted"] is False):
        log_error(
                "Incorrect response (HTTP/1.1 " + response.status_code +
                ") from GET /logout: " + str(response_body)
        )
        sys.exit(1)

    log_debug("Successfully logged out.")

if __name__ == "__main__":
    auth_token = get_auth_token()
    logout(auth_token)
