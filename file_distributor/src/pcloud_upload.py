#!/usr/bin/env python3
#
# This Python 3 script authenticates with pCloud and downloads a file.
# Authentication details are set in a configuration file.

import configparser
import hashlib
import requests
import sys
import time

config_filename = "file_distributor.cfg"

class Logger:
    """Outputs formatted log messages."""

    # Change this to True to enable output debug logging for this module.
    print_debug_logs = True

    @classmethod
    def __log(self, log_level, message):
        """Outputs a formatted log message if logging is activated.

        Parameters:
        log_level -- String. Severity of the log message.
        message -- String. Message to be logged.
        """
        if self.print_debug_logs:
            print(
                    "[ " +
                    time.strftime("%Y-%m-%d %H:%M:%S") +
                    " | " +
                    log_level +
                    " ] " +
                    message
            )

    @staticmethod
    def debug(message):
        """Outputs a debug level log message."""
        Logger.__log("DEBUG  ", message)

    @staticmethod
    def success(message):
        """Outputs a success level log message."""
        Logger.__log("SUCCESS", message)

    @staticmethod
    def error(message):
        """Outputs a error level log message."""
        Logger.__log("ERROR  ", message)

class PCloud:
    """Provides simple methods to access the pCloud API."""

    def __init__(self):
        """Variable initializer."""
        self.auth_token = None

    def __must_be_logged_in(self):
        """Checks that the authentication token is present from a login.

        Throws:
        Exception -- If the token is not present.
        """
        if self.auth_token == None:
            raise Exception("Cannot perform this operation while logged out.")

    def __must_be_logged_out(self):
        """Checks that the authentication token is not present.

        Throws:
        Exception -- If the token is present.
        """
        if self.auth_token != None:
            raise Exception("Cannot perform this operation while logged in.")

    def __api_call(self, rest_api, url, params=None, file_path_upload=None,
            response_body_validity_check=None):
        """Sends a REST API call designed for the pCloud service.

        The authentication token will automatically be added to the REST
        parameters, if it exists.

        Parameters:
        rest_api -- String. Name of the API called. Used for logging and errors.
            E.g. "GET /data"
        url -- String. URL of the API. E.g. "http://www.google.com"
        params -- Dictionary (optional). Mapping between REST parameter names
            and values.
        file_path_upload -- String (optional). If passed, the request will be a
            POST request and the file at the given path will be sent;
            else, the request will be a GET request.

        Throws:
        Exception -- If the response from the API is invalid.
        """
        if params is None:
            params = dict()
        if response_body_validity_check is None:
            response_body_validity_check = True
        params["auth"] = self.auth_token

        if file_path_upload is None:
            response = requests.get(url=url, params=params)
        else:
            response = requests.post(url=url, params=params,
                    files={file_path_upload: open(file_path_upload, "rb")}
            )
        response_body = response.json()

        Logger.debug(rest_api + " status code: " + str(response.status_code))
        Logger.debug(rest_api + " response body: " + str(response_body))
        if(response.status_code != requests.codes.ok or
                response_body_validity_check(response_body) is False):
            error_message = "Incorrect response (HTTP/1.1 " + \
                    str(response.status_code) + ") from " + rest_api + \
                    ": " + str(response_body)
            Logger.error(error_message)
            raise Exception(error_message)

        return response_body

    def __get_digest(self):
        """Retrieves a digest from the API.

        Returns a string containing the digest.
        """
        response_body = self.__api_call(
                "GET /getdigest", "https://api.pcloud.com/getdigest",
                response_body_validity_check=lambda response_body:
                        response_body is not None and
                        "result" in response_body and
                        response_body["result"] == 0 and
                        "digest" in response_body and
                        response_body["digest"] is not None
        )
        return response_body["digest"]

    @staticmethod
    def __sha1_encode(val):
        """Encodes a value using SHA1 and returns it in hexadecimal format.

        Parameters:
        val -- String. Value to encode.

        Returns a string containing the encoded value.
        """
        return hashlib.sha1(val.encode("utf-8")).hexdigest()

    def login(self, username, password):
        """Logs into pCloud.

        Fails if already logged in.
        If successful, the authentication token will be saved in the object.

        Parameters:
        username -- String. Username of the pCloud account (usually the email).
        password -- String. Password of the pCloud account.
        """
        self.__must_be_logged_out()

        digest = self.__get_digest()
        password_digest = PCloud.__sha1_encode(
                password +
                PCloud.__sha1_encode(username.lower()) +
                digest
        )

        request_params = dict(
                getauth = 1,
                username = username,
                digest = digest,
                passworddigest = password_digest
        )
        response_body = self.__api_call(
                "GET /userinfo",
                "https://api.pcloud.com/userinfo",
                request_params,
                response_body_validity_check=lambda response_body:
                        response_body is not None and
                        "auth" in response_body and
                        response_body["auth"] is not None
        )

        self.auth_token = response_body["auth"]
        Logger.debug("Successfully logged in.")

    def upload_file(self, file_path_local, dir_path_pcloud, file_name_pcloud):
        """Uploads a file to a pCloud account.

        Fails if not logged in.

        Parameters:
        file_path_local -- String. Path to the file locally (relative to the
            location where this script was executed).
        dir_path_pcloud -- String (optional). Path to the file in pCloud.
            Should not include the filename.
            If the root folder is the target, this should be None or an
            empty string.
        file_name_pcloud -- String. Name of the file.
        """
        self.__must_be_logged_in()

        if dir_path_pcloud == "":  # Will be empty string for root folder
            dir_path_pcloud = None

        request_params = dict(
                path = dir_path_pcloud,
                filename = file_name_pcloud,
                nopartial = 1
        )
        self.__api_call(
                "POST /uploadfile", "https://api.pcloud.com/uploadfile",
                request_params, file_path_local, lambda response_body:
                        response_body is not None and
                        "result" in response_body and
                        response_body["result"] == 0 and
                        "fileids" in response_body and
                        len(response_body["fileids"]) > 0
        )
        Logger.success("File " + file_name_pcloud + " uploaded to pCloud.")

    def logout(self):
        """Logs out of the account.

        Fails if already logged out.
        The authentication token stored in this object will be cleared.
        """
        self.__must_be_logged_in()

        if self.auth_token is None:
            Logger.error("Logout attempt failed because you are not logged in.")
            sys.exit(1)
        self.__api_call(
                "GET /logout", "https://api.pcloud.com/logout",
                response_body_validity_check=lambda response_body:
                        response_body is not None and
                        "auth_deleted" in response_body and
                        response_body["auth_deleted"] is not None and
                        response_body["auth_deleted"] is True
        )
        self.auth_token = None
        Logger.debug("Successfully logged out.")

def main():
    config = configparser.ConfigParser()
    config.read(config_filename)

    section_local = "Local"
    file_path_local = config[section_local]["file_path"]

    section_pcloud = "pCloud"
    username_pcloud = config[section_pcloud]["username"]
    password_pcloud = config[section_pcloud]["password"]
    dir_path_pcloud = config[section_pcloud]["dir_path"]
    file_name_pcloud = config[section_pcloud]["file_name"]

    p = PCloud()
    p.login(username_pcloud, password_pcloud)
    p.upload_file(file_path_local, dir_path_pcloud, file_name_pcloud)
    p.logout()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        Logger.error("File not uploaded to pCloud: " + str(e))
