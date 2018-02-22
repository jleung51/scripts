#!/usr/bin/env python3
# This Python 3 script retrieves event data from a Google Calendar, formats
# it to be simpler, categorizes the events according to specific criteria,
# and creates a JSON file with the event data and the list of categories.

import configparser
import json
import logging
import os

from google_api import GoogleCalendarApi

def __logger():
    """Retrieves the module-level logger object."""
    return logging.getLogger(__name__)

def initialize_logger():
    """Initializes the settings for the logger object."""
    logging.basicConfig(filename = __name__ + ".log")

    logger = __logger()
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[ %(asctime)s | %(levelname)s ] %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

def remove_events_without_price(events, currency_symbol):
    """Removes events which do not have a description or start with symbol."""
    remove_list = []
    for e in events:

        if "description" not in e:
            remove_list.append(e)
            continue
        # Description must begin with a specific currency symbol
        elif not e["description"].startswith(currency_symbol):
            remove_list.append(e)

    for e in remove_list:
        events.remove(e)

def description_to_price(events, currency_symbol):
    """Isolates the price from the description which is deleted.

    Assumes that the price is at the beginning of the description.
    """
    for e in events:
        price = ""
        for char in e["description"]:
            if currency_symbol != char and not char.isdigit():
                break
            price += char
        e["price"] = price
        del e["description"]

def simplify_start_end_times(events):
    """Removes the sublevel for the start/end times of each event."""
    for e in events:
        try:
            e["start"] = e["start"]["dateTime"]
        except KeyError:
            pass

        try:
            e["end"] = e["end"]["dateTime"]
        except KeyError:
            pass

def categorize(events):
    """Assigns a category for each event by its summary (event name).

    Should be modified as per the specifics of each event and calendar.
    """
    for e in events:
        name = e["summary"].lower()

        if "check" in name:
            e["category"] = "lodging"

        elif "transit" in name \
                or "station" in name \
                or "line" in name \
                or "bus" in name:
            e["category"] = "transportation"

        elif "breakfast" in name \
                or "lunch" in name \
                or "dinner" in name:
            e["category"] = "meals"

        elif "eat" in name \
                or "beverage" in name \
                or "coffee" in name \
                or "tea" in name \
                or "water" in name \
                or "soda" in name \
                or "cola" in name \
                or "juice" in name \
                or "beer" in name \
                or "pocari sweat" in name \
                or "noodles" in name \
                or "pocky" in name \
                or "taiyaki" in name:
            e["category"] = "snacks_drinks"

        elif "visit" in name \
                or "hot springs" in name:
            e["category"] = "entrance"

        elif "buy" in name \
                or "rent" in name \
                or "clothes" in name:
            e["category"] = "purchases"

        else:
            e["category"] = "uncategorized"

def sort_into_sections(events, categories):
    """Separates events into their distinct (already-defined) categories."""

    categorized = {}
    for c in categories:
        categorized[c] = []

    for e in events:
        categorized[e["category"]].append(e)

    return categorized

def main():
    location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
    config_filename = os.path.join(location, "gcalendar_event_scraper.cfg")
    config = configparser.ConfigParser()
    config.read(config_filename)
    config = config["Google Calendar Events"]

    initialize_logger()

    g = GoogleCalendarApi()

    # Use this to view all the available calendars and their IDs
    # print(json.dumps(g.list_calendars(), indent=4))

    events = g.list_events(config["calendar_id"], config["start_time"],
            config["end_time"], config["time_zone"])

    __logger().debug("Retrieved events from Google Calendar.")

    remove_events_without_price(events, config["currency_symbol"])
    description_to_price(events, config["currency_symbol"])
    simplify_start_end_times(events)

    categorize(events)

    categories = [
        "lodging",
        "transportation",
        "meals",
        "snacks_drinks",
        "entrance",
        "purchases",
        "uncategorized"
    ]

    # To view the categorization clearly
    # categorized = sort_into_sections(events, categories)

    data = {
        "categories": categories,
        "events": events
    }
    filename = "data.json"
    __logger().debug("Writing event data to " + filename)
    with open(filename, 'w') as output_file:
        json.dump(data, output_file,
                indent=4, ensure_ascii=False, sort_keys=True)

    __logger().debug("Successfully wrote event data to " + filename)

if __name__ == "__main__":
    main()
