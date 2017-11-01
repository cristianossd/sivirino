# :older_man: sivirino
A simple email validation API built in Python. It validates emails by looking at their format using regex and by checking its existence in its mail server through SMTP.

### USAGE
Emails should by sent one at a time by a GET request to the following route:

| Name | Path | Method | Purpose |
| ------ | ------ | ------ | ------ |
| Validate Email | /api/email/\<email\>/validate | GET | Validates the email in the \<email\> parameter |

Valid emails will return a **200 OK** response while invalid ones will return a **500 Internal Server Error** one.
