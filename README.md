# Traffic Monitor

Python 3 script which uses the [Microsoft/Bing Maps Traffic API](https://msdn.microsoft.com/en-us/library/hh441725.aspx) to notify a user if there are any traffic disruptions within a range of coordinates.

Email notifications are configurable using the [Gmail API](https://developers.google.com/gmail/api/).

## Setup

### Traffic Data

TODO

### Notifications

#### Emails from a Gmail account

Set the variables beginning with `mail_` to your preferred application name, the Gmail account which your notification emails will be sent from, and the destination email account which your notification emails will be sent to.

Install the following pip 3 dependencies:
* google-api-python-client

From the [Gmail Developer APIs](https://developers.google.com/gmail/api/quickstart/python), follow **Step 1: Turn on the Gmail API** to get an authentication key for the Gmail account from which you'll be sending the email. Make sure you keep `client_secret.json` in the same directory as the traffic monitor script.

During the first time you run the script, it should show you a URL and ask you to retrieve the verification code. Follow the instructions so you can properly authenticate your script to use your Gmail account. This will not be necessary on subsequent calls.
