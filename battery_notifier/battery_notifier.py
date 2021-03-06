#!/usr/bin/env python3
#
# This Python 3 program checks for a change in battery level since the last
# time this program was run, and sends an alert when the battery level
# decreases below a custom threshold.

import configparser
import os
import subprocess
import sys
import time

# Custom modules:
from logger import Logger
from slack_messenger import SlackMessenger

# Change the values in this array to modify at what percentages the
# notification should be sent.
alert_percentages = [20, 50]

def report_battery_level(slack_config, battery_level):
    if slack_config.getboolean("reporting") is True:
        slack_messenger = SlackMessenger(
                slack_config["report_slack_token"],
                slack_config["report_channel"],
                slack_config["report_slackbot_name"]
        )
        slack_messenger.message(
                "Current laptop battery level: " + str(battery_level) + "%."
        )

def alert_battery_level(slack_config, alert_level):
    slack_messenger = SlackMessenger(
            slack_config["alert_slack_token"],
            slack_config["alert_channel"],
            slack_config["alert_slackbot_name"]
    )
    slack_messenger.notify(
            slack_config["alert_list"],
            "Laptop battery is below " + str(alert_level) + "%."
    )

def alert_error(slack_config):
    slack_messenger = SlackMessenger(
            slack_config["alert_slack_token"],
            slack_config["alert_channel"],
            slack_config["alert_slackbot_name"]
    )
    slack_messenger.notify(
            slack_config["alert_list"],
            "Internal error for Battery Notifier, please check the logs."
    )

def run_cmd(args):
    '''Executes a set of arguments in the command line.

    Arguments:
        args -- Arguments to execute.
    Returns:
        string -- Output (stdout) from the execution.
    '''
    return subprocess.run(args, stdout=subprocess.PIPE).stdout.decode("utf-8")

def find_line_with(lines, str):
    '''Returns the first line with the given search term.

    Arguments:
        lines (string) -- Set of lines, separated by newlines.
        str (string) -- The given search term.
    Returns:
        string -- The first occurrence of a line containing the search term.s
    '''
    for line in lines.split("\n"):
        if str in line:
            return line

def get_battery_percentage():
    '''Returns the current battery level in percent.

    Returns:
        int -- The current battery level in percent.
    '''
    # Parse power data from OS
    power_files = run_cmd(["upower", "-e"])
    power_file = find_line_with(power_files, "BAT")

    power_data = run_cmd(["upower", "-i", power_file])
    percentage_line = find_line_with(power_data, "percentage")

    # Parse percentage from string with various characters into number
    current_percent = ""
    for char in percentage_line:
        if char.isdigit():
            current_percent += char

    return int(current_percent)

def main(config):
    slack_config = config["Slack"]

    current_percent = get_battery_percentage()

    Logger.debug("Current battery: " + str(current_percent) + "%")
    report_battery_level(slack_config, current_percent)

    battery_level_filename = "/tmp/last_battery_level"

    # Open file for reading and writing, or create one if it does not exist
    try:
        # Read and write existing file
        file = open(battery_level_filename, mode='r+')
    except IOError:
        Logger.debug("Battery state file does not exist; creating new file.")

        # Read and write new file
        file = open(battery_level_filename, mode='x+')
        file.write(str(current_percent))
        file.flush()
        file.seek(0)  # Rewind to beginning of file

    file_contents = file.read()
    try:
        last_percent = int(file_contents)
    except ValueError:
        Logger.error("Last battery level could not be parsed. Contents: ")
        Logger.error(file.read(file_contents))
        Logger.error("Recreating battery state file.")
        last_percent = current_percent

    # # Tester
    # current_percent = 0
    # last_percent = 100

    if current_percent < last_percent:
        alert_percentages.sort()  # Only alert for the lowest percentage
        for i in alert_percentages:
            if current_percent <= i and i < last_percent:
                Logger.info("Alert: Battery is below " + str(i) + "%.")
                alert_battery_level(slack_config, i)
                break;

    # Replace previous percentage with new percentage
    file.seek(0)
    file.write(str(current_percent))
    file.truncate()

    file.close()

if __name__ == "__main__":
    location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
    config_filename = os.path.join(location, "battery_notifier.cfg")
    config = configparser.ConfigParser()
    config.read(config_filename)
    try:
        main(config)
    except Exception as e:
        alert_error(config["Slack"])
        raise
