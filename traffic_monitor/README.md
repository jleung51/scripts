# Traffic Monitor

Python 3 script which uses the [Microsoft/Bing Maps Traffic API](https://msdn.microsoft.com/en-us/library/hh441725.aspx) to notify a user if there are any traffic disruptions within a range of coordinates.

Configurable mail notifications are set up to use the [Gmail API](https://developers.google.com/gmail/api/). By default, the subject is `Traffic Incident Alert` and the message body is formatted like this:
```
Serious traffic disruption. Uncategorized alert at 116th St/Exit 202 - Exit ramp closed. Coordinates: (48.09642, -122.18471).

Moderate traffic disruption. Road hazard at Pavilion-Clinton Rd - Incident. Coordinates: (50.742394, -121.864216).

Moderate traffic disruption. Road hazard at Fountain Valley Hwy - Incident. Coordinates: (50.880798, -121.829067).


Sincerely,

- Your friendly neighborhood Traffic Monitor
```

## Setup

Setup the [Logger](https://github.com/jleung51/scripts/tree/master/modules/logger) module in this directory.

Edit the script `traffic_monitor.py` to configure the authentication and authorization variables at the beginning of the file. Each variable has its own explanation; read them carefully.

### Email Setup

Set up the [Gmail Sender](https://github.com/jleung51/scripts/tree/master/gmail_sender) module in this directory. Set the email configuration variables in `traffic_monitor.py` accordingly.

### Reports to a Slack Channel

Optionally, you can choose to set up reports to a Slack channel.

Set `report = True` in the script variables.

Set up the [Slack Logger](https://github.com/jleung51/scripts/tree/master/slack_logger) module in this directory.

Fill in the remaining Slack variables in the script as necessary.

## Execution

Simply run:

```
./traffic_monitor.py
```
