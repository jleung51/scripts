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
from slack_logger import SlackLogger

# Change the values in this array to modify at what percentages the
# notification should be sent.
alert_percentages = [20, 50]

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
    def info(message):
        """Outputs an info level log message."""
        Logger.__log("INFO   ", message)

    @staticmethod
    def success(message):
        """Outputs a success level log message."""
        Logger.__log("SUCCESS", message)

    @staticmethod
    def error(message):
        """Outputs a error level log message."""
        Logger.__log("ERROR  ", message)

def report_battery_level(slack_config, battery_level):
    slack_logger = SlackLogger(
            slack_config["report_slack_token"],
            slack_config["report_channel"],
            slack_config["report_slackbot_name"]
    )
    slack_logger.report(
            "SUCCESS", "Current battery level: " + str(battery_level) + "%."
    )

def report_battery_level_alert(slack_config, alert_level):
    slack_logger = SlackLogger(
            slack_config["report_slack_token"],
            slack_config["report_channel"],
            slack_config["report_slackbot_name"]
    )
    slack_logger.report(
            "ALERT FOR " + slack_config["report_alert_list"],
            "Battery is below " + str(alert_level) + "%."
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

def main():
    config_filename = "battery_notifier.cfg"
    config = configparser.ConfigParser()
    config.read(config_filename)

    slack_config = config["Slack"]

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
    current_percent = int(current_percent)

    Logger.debug("Current battery: " + str(current_percent) + "%")
    report_battery_level(slack_config, current_percent)

    # Place battery state file in the same directory
    location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
    battery_state_filename = os.path.join(location, 'battery_state')

    # Open file for reading and writing, or create one if it does not exist
    try:
        # Read and write existing file
        file = open(battery_state_filename, mode='r+')
    except IOError:
        Logger.debug("Battery state file does not exist; creating new file.")

        # Read and write new file
        file = open(battery_state_filename, mode='x+')
        file.write(str(current_percent))
        file.flush()
        file.seek(0)  # Rewind to beginning of file

    file_contents = file.read()
    try:
        last_percent = int(file_contents)
    except ValueError:
        Logger.error("Battery state file could not be parsed. Contents: ")
        Logger.error(file.read(file_contents))
        Logger.error("Recreating battery state file.")
        last_percent = current_percent

    if current_percent < last_percent:
        alert_percentages.sort()  # Only alert for the lowest percentage
        for i in alert_percentages:
            if current_percent <= i and i < last_percent:
                Logger.info("Alert: Battery is below " + str(i) + "%.")
                report_battery_level_alert(slack_config, i)
                break;

    # Replace previous percentage with new percentage
    file.seek(0)
    file.write(str(current_percent))
    file.truncate()

    file.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        Logger.error(
                "Script experienced an error and could not complete: " + str(e)
        )
