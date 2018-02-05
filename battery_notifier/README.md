# Battery Notifier

Python 3 script which sends an alert to a Slack channel if a battery level decreases below a certain threshold.

## Setup

Prerequisites:
* Python 3 installed on your system
* The pip dependencies `configparser` and `slackclient` installed
* A Slack team with a channel which the bot will send an alert to
* A Slack team with a channel which the bot will send a report to (optional)

Setup the [Logger](https://github.com/jleung51/scripts/tree/master/modules/logger) and [Slack Messenger](https://github.com/jleung51/scripts/tree/master/modules/slack_messenger) modules in this directory, complete the dependencies, and set up the Slack team and bot.

Create a new configuration file (which will not be tracked by Git):
```
cp battery_notifier.cfg.template battery_notifier.cfg
```

Edit the new configuration file to include the Slack credentials.

Customize the list of thresholds in `battery_notifier.py` for which an alert should be sent.

## Execution

```
./battery_notifier.py
```

On the first time that the script is activated, no alert will be sent. An alert is only created when
