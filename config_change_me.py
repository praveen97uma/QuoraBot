"""
Change the name of this file to config.py
"""

#Number of page down key press events selenium should send on quora page
NO_OF_PAGEDOWNS = 10

QUORA_USERNAME = ""
QUORA_PASSWORD = ""

GMAIL_USERNAME = ""
GMAIL_PASSWORD = ""

GMAIL_SMTP_HOST = 'smtp.gmail.com'
GMAIL_SMTP_PORT = 587

EMAIL_SUBJECT = "New Quora Questions"
RECIPIENT_ADDRESS = ""

EMAIL_HEADERS = "\r\n".join(["from: My Quora Bot", 
							"subject: %s"%(EMAIL_SUBJECT), 
							"to: %s"%(RECIPIENT_ADDRESS),
							"mime-version: 1.0",
							"content-type: text/html"])

							