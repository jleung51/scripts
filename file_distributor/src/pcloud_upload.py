#!/usr/bin/env python3
#
# This Python 3 script authenticates with pCloud and downloads a file.
# Authentication details are set in a configuration file.

import configparser

# Custom imports
from logger import Logger
from pcloud_api import PCloudApi

config_filename = "file_distributor.cfg"

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

    p = PCloudApi()
    p.login(username_pcloud, password_pcloud)
    p.upload_file(file_path_local, dir_path_pcloud, file_name_pcloud)
    p.logout()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        Logger.error("File not uploaded to pCloud: " + str(e))
