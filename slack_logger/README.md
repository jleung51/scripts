# Slack Logger

Python 3 module which provides easy functionality for customized operation status reports to a Slack channel.

## Example

The Slack message will be displayed as follows:

> **Custom Slackbot Name**
> > _2016-12-23 20:20:28_  
> > Operation status: OPERATION_STATUS  
> > MESSAGE_TEXT

## Setup

### Dependencies

Install the following pip 3 dependency:
* slackclient

### Slack Setup

[Create a Slackbot bot](https://api.slack.com/bot-users) in the Slack team you want to send Slack messages to. Once you are finished the setup, navigate to the _Integration Settings_ section (if you lost the page, it's located at `App Directory > Browse Apps > Custom Integrations > Bots`) and save the API Token displayed there. You will need this API token to authenticate your bot.

Invite your Slack bot to the channel they should send a message to.

### Reporting from the Program

Add the `slack_logger.py` module to the directory of the Python program which needs to log reports to Slack. Import the module in your program:

```
from slack_logger import SlackLogger
```

Instantiate a SlackLogger object:
```
slack_logger = SlackLogger(slack_api_token, slack_channel, slackbot_name)
```

And send a report to the Slack team:
```
slack_logger.report(operation_status, message_text)
```

For detailed information on the parameters and usage, see the documentation in the `SlackLogger` class.

### Configuration

If you want to enable debug logging output, change the value of the variable `print_debug_logs` in `slack_logger.py` to True.

Debug output is formatted like so:
```
[ 2016-12-24 22:44:41 | DEBUG   ] Slack report sent.
```
