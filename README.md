# Slackbot Messager

Python 3 script which sends a single, customizable message to a Slack channel. The script can be easily set up as a cron job so it posts a message on a consistent basis.

## Setup

Prerequisites:
* Python 3 installed on your system
* The pip dependency `slackclient` installed
* A Slack team with a channel which the bot will send a message to

[Create a Slackbot bot](https://api.slack.com/bot-users) in the Slack team you want to send Slack messages to. Once you are finished the setup, navigate to the _Integration Settings_ section (if you lost the page, it's located at `App Directory > Browse Apps > Custom Integrations > Bots`) and save the API Token displayed there. You will need this API token to authenticate your bot.

Invite your Slack bot to the channel they should send a message to.

Copy the `slackbot_messager.py` script to a new file. Don't edit and commit the original `slackbot_messager.py` because it will contain sensitive authentication data.

Edit the new file and fill in the empty fields at the top as described. If you do not want a report to be sent to another Slack team/channel (for error monitoring), simply leave `report = False` and don't set the following `report_` variables.

You can now simply execute the script and see the message sent to your Slack team!
