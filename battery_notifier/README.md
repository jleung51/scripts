# Battery Notifier

Python 3 script which sends an alert to a Slack channel if a battery level decreases below a certain threshold.

## Setup

Prerequisites:
* Python 3 installed on your system
* The pip dependency `slackclient` installed
* A Slack team with a channel which the bot will send a message to

Install the pip dependency:
```
pip3 install slackclient
```

Set up the [Slack Logger](https://github.com/jleung51/scripts/tree/master/slack_logger) script in this directory.

Create a new configuration file (which will not be tracked by Git):
```
cp battery_notifier.cfg.template battery_notifier.cfg
```

Edit the new configuration file to include the Slack credentials.

## Execution

```
./battery_notifier.py
```

On the first time that the script is activated, no alert will be sent. An alert is only created when
