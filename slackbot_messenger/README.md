# Slackbot Messenger

Python 3 script which sends a single, customizable message to a Slack channel. The script can be easily set up as a cron job so it posts a message on a consistent basis.

## Setup

Prerequisites:
* Python 3 installed on your system
* The pip dependency `slackclient` installed
* A Slack team with a channel which the bot will send the message to
* A Slack team with a channel which the bot will send a report to (optional)

Complete the _Setup_ sections of the following Python modules from [Utilities](https://github.com/jleung51/utilities) to set them up in this directory:

* [Slack Messenger](https://github.com/jleung51/utilities/tree/master/python_modules/slack_messenger)

### Script Setup

Copy the `slackbot_messenger.py` script to a new file. Don't edit and commit the original `slackbot_messenger.py` because it will contain sensitive authentication data.

Edit the new file and fill in the empty fields at the top as described.

### Reports to a Slack Channel

Optionally, you can choose to set up reports to a Slack channel.

Set `report = True` in the script variables.

Fill in the remaining report variables in the script as necessary.

## Execution

Simply run:

```
./slackbot_messenger.py "message"
```

where `message` is the text to send to the Slack channel.
