#!/usr/bin/env python3
#
# This Python 3 program checks for a change in battery level since the last
# time this program was run, and sends an alert when the battery level
# decreases below a custom threshold.

import os
import subprocess
import sys

# Change the values in this array to modify at what percentages the
# notification should be sent.
alert_percentages = [20, 50]

# Functions:

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

    print("Current battery: " + str(current_percent) + "%")

    # Place battery state file in the same directory
    location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
    battery_state_filename = os.path.join(location, 'battery_state')

    # Open file for reading and writing, or create one if it does not exist
    try:
        # Read and write existing file
        file = open(battery_state_filename, mode='r+')
    except IOError:
        print("Battery state file does not exist; creating new file.")

        # Read and write new file
        file = open(battery_state_filename, mode='x+')
        file.write(str(current_percent))
        file.flush()
        file.seek(0)  # Rewind to beginning of file

    last_percent = int(file.read())
    if current_percent < last_percent:
        alert_percentages.sort()  # Only alert for the lowest percentage
        for i in alert_percentages:
            if current_percent < i and i < last_percent:
                print("Alert: Battery is below " + str(i) + "%.")
                break;

    # Replace previous percentage with new percentage
    file.seek(0)
    file.write(str(current_percent))
    file.truncate()

    file.close()

main()
