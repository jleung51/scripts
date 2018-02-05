#!/usr/bin/env python3
#
# This Python 3 module provides functions to output formatted logs.
#
# The following log levels are currently supported:
#   DEBUG
#   INFO
#   SUCCESS
#   ERROR

import time

# Change this to False to disable all output logging for this module.
print_logs = True

class Logger:
    """Outputs formatted log messages."""

    @classmethod
    def __log(self, log_level, message):
        """Outputs a formatted log message if logging is activated.
        Parameters:
        log_level -- String. Severity of the log message.
        message -- String. Message to be logged.
        """
        if print_logs:
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
