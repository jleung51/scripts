#!/usr/bin/env python3

import configparser
import hashlib
import requests
import sys
import time

config_filename = "file_distributor.cfg"

class Logger:
    # Change this to True to enable output debug logging for this module.
    print_debug_logs = True

    @classmethod
    def __log(self, log_level, message):
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
        Logger.__log("DEBUG  ", message)

    @staticmethod
    def success(message):
        Logger.__log("SUCCESS", message)

    @staticmethod
    def log_error(message):
        Logger.__log("ERROR  ", message)

class PCloud:
    def __init__(self):
        self.auth_token = None

    def __must_be_logged_in(self):
        if self.auth_token == None:
            raise Exception("Cannot perform this operation while logged out.")

    def __must_be_logged_out(self):
        if self.auth_token != None:
            raise Exception("Cannot perform this operation while logged in.")

    def __api_call(self, rest_api, url, params=None, file_path_upload=None,
            response_body_validity_check=None):
        """Makes a REST API call designed for the pCloud service.

        The authentication token will automatically be added to the parameters,
        if it exists.
        Parameters:
        file_path_upload -- String. If passed, the request will be a
            POST request; else, the request will be a GET request.
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
            Logger.error(
                    "Incorrect response (HTTP/1.1 " + str(response.status_code)
                    + ") from " + rest_api + ": " + str(response_body)
            )
            sys.exit(1)

        return response_body

    def __get_digest(self):
        response_body = self.__api_call(
                "GET /getdigest", "https://api.pcloud.com/getdigest",
                response_body_validity_check=lambda response_body:
                        response_body is not None and
                        response_body["result"] == 0 and
                        response_body["digest"] is not None
        )
        return response_body["digest"]

    @staticmethod
    def __sha1_encode(val):
        return hashlib.sha1(val.encode("utf-8")).hexdigest()

    def login(self, username, password):
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
                        response_body["auth"] is not None
        )

        self.auth_token = response_body["auth"]
        Logger.debug("Successfully logged in.")

    def upload_file(self, file_path_local, dir_path_pcloud, file_name_pcloud):
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
                        response_body["result"] is not None and
                        response_body["result"] == 0 and
                        response_body["fileids"] is not None and
                        len(response_body["fileids"]) > 0
        )
        Logger.success("File " + file_name_pcloud + " uploaded to pCloud.")

    def logout(self):
        self.__must_be_logged_in()

        if self.auth_token is None:
            Logger.error("Logout attempt failed because you are not logged in.")
            sys.exit(1)
        self.__api_call(
                "GET /logout", "https://api.pcloud.com/logout",
                response_body_validity_check=lambda response_body:
                        response_body is not None and
                        response_body["auth_deleted"] is not None and
                        response_body["auth_deleted"] is True
        )
        self.auth_token = None
        Logger.debug("Successfully logged out.")

if __name__ == "__main__":
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
