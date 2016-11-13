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

Execution details are outputted in a loggable format like so:
```
[ 2016-11-12 22:27:24 | DEBUG   ] Mail source:  email@email.com
[ 2016-11-12 22:27:24 | DEBUG   ] Mail target:  email@email.com
[ 2016-11-12 22:27:24 | DEBUG   ] Mail subject: Traffic Incident Alert
[ 2016-11-12 22:27:24 | DEBUG   ] Mail message: Serious traffic disruption. Uncategorized alert at 116th St/Exit 202 - Exit ramp closed. Coordinates: (48.09642, -122.18471).[newline][newline]Moderate traffic disruption. Road hazard at Pavilion-Clinton Rd - Incident. Coordinates: (50.742394, -121.864216).[newline][newline]Moderate traffic disruption. Road hazard at Fountain Valley Hwy - Incident. Coordinates: (50.880798, -121.829067).[newline][newline][newline]Sincerely,[newline][newline]- Your friendly neighborhood Traffic Monitor
[ 2016-11-12 22:27:25 | DEBUG   ] Mail sent.
[ 2016-11-12 22:27:25 | SUCCESS ] Operation completed.
```

## Setup

Edit the script `traffic-monitor.py` to configure the authentication and authorization variables at the beginning of the file. Each variable has its own explanation; read them carefully. Unless you would like to enable reports to a Slack channel (in which case you would set `report` to `True`), there is no need to fill in the Slack configuration variables.

### Authorizing Emails from a Gmail account

Install the following pip 3 dependencies:
* google-api-python-client
* httplib2

From the [Gmail Developer APIs](https://developers.google.com/gmail/api/quickstart/python), follow **Step 1: Turn on the Gmail API** to get an authentication key for the Gmail account from which you'll be sending the email. Make sure you keep `client_secret.json` in the same directory as the traffic monitor script.

During the first time you run the script, Gmail will display a URL and ask you to retrieve the verification code. Follow the instructions so you can properly authenticate your script to use your Gmail account. This will not be necessary on subsequent calls, as long as you do not modify the autogenerated file `generated_credentials.json`.

### Reports to a Slack Channel

Optionally, you can choose to set up reports to a Slack channel.

Install the following pip 3 dependency:
* slackclient

Set `report = True` in the script variables.

[Create a Slackbot bot](https://api.slack.com/bot-users) in the Slack team you want to send Slack messages to. Once you are finished the setup, navigate to the _Integration Settings_ section (if you lost the page, it's located at `App Directory > Browse Apps > Custom Integrations > Bots`) and save the API Token displayed there. You will need this API token to authenticate your bot.

Invite your Slack bot to the channel they should send a message to.

Fill in the remaining Slack variables in the script as necessary.

## Execution

Simply run:

```
./traffic-monitor.py
```
