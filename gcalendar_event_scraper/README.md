# Google Calendar Event Scraper

Python 3 script which generates a JSON file with event data retrieved from Google Calendar, simplified, and categorized with specifically subjective criteria.

Only events with a description which begins with a specific currency symbol (defined in the configuration) and then a price will be retrieved.

## Setup

### Custom Modules

Complete the _Setup_ sections of the following Python module from [Utilities](https://github.com/jleung51/utilities) to set it up in this directory:

* [Google API](https://github.com/jleung51/utilities/tree/master/python_modules/api_wrappers/google_api)

### Configuration

Create a new configuration file (which will not be tracked by Git):

```
cp gcalendar_event_scraper.cfg.template gcalendar_event_scraper.cfg
```

Edit the new configuration file to define the specific event data to request.

#### Calendar ID

The events must be scraped from a single calendar in Google Calendar, identified uniquely by the calendar ID. The main calendar has the calendar ID `primary`. To find the ID of any other calendar, uncomment this line in the script:

```
print(json.dumps(g.list_calendars(), indent=4))
```

And run the script to find the ID of the specific calendar.

## Execution

```
./gcalendar_event_scraper.py
```

The resulting data will be written to `data.json`, and will be formatted like so:

```json
{
    "categories": [
        "lodging",
        "transportation",
        "meals",
        "snacks_drinks",
        "entrance",
        "purchases",
        "uncategorized"
    ],
    "events": [
        {
            "start": "2017-05-09T20:15:00+09:00",
            "end": "2017-05-09T21:15:00+09:00",
            "category": "lodging",
            "location": "Imano Tokyo Hostel",
            "summary": "Check into Imano Hostel ",
            "description": "¥11300"
        }
    ]
}
```
