# Slack Messenger

Python 3 module which provides easy functionality for customized messages to a Slack channel.

## Setup

### Dependencies

Install the following pip 3 dependency:
* slackclient

Setup the [Logger](https://github.com/jleung51/scripts/tree/master/modules/logger) module in this directory.

### Slack Setup

[Create a Slackbot bot](https://api.slack.com/bot-users) in the Slack team you want to send Slack messages to. Once you are finished the setup, navigate to the _Integration Settings_ section (if you lost the page, it's located at `App Directory > Browse Apps > Custom Integrations > Bots`) and save the API Token displayed there. You will need this API token to authenticate your bot.

Invite your Slack bot to the channel they should send a message to.

## Usage

Add the `slack_messenger.py` module to the directory of the Python program which needs to log reports to Slack. Import the module in your program:

```
from slack_messenger import SlackMessenger
```

Instantiate a SlackMessenger object:
```
slack_messenger = SlackMessenger(slack_api_token, slack_channel, slackbot_name)
```

And send a message in a specific format to the Slack team:
```
slack_messenger.message(message_text)
slack_messenger.notify("@jleung51 | @jleung52", message_text)
slack_messenger.operation_report("*SUCCESS*", message_text)
```

For detailed information on the parameters and usage, see the documentation in the `SlackMessenger` class.

### Configuration

If you want to enable debug logging output, change the value of the variable `print_debug_logs` in `slack_messenger.py` to True.

Debug output is formatted like so:
```
[ 2016-12-24 22:44:41 | DEBUG   ] Message sent.
```
