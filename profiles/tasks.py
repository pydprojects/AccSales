from django.conf import settings

import requests
from celery import shared_task


@shared_task
def send_email(recipient_mail, text):
    mail_subject = 'Account activation.'
    sender = getattr(settings, 'EMAIL_HOST_USER', None)
    return requests.post(
        "https://api.mailgun.net/v3/sandbox4dcc7b1a3b0e4018bde85dd3592b0dfa.mailgun.org/messages",
        # Need API-Key from https://app.mailgun.com/app/account/security/api_keys
        auth=("api", ""),
        data={"from": f"TestTask robot <{sender}>",
              "to": [recipient_mail],
              "subject": mail_subject,
              "text": text})
