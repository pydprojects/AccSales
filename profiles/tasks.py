from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from celery import shared_task

from .tokens import account_activation_token


@shared_task
def send_email_activation(user, domain, email):
    subject = 'Активация аккаунта.'
    message = render_to_string('profiles/confirm_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user)),
        'token': account_activation_token.make_token(user),
    })
    sender = getattr(settings, 'EMAIL_HOST_USER', None)
    send_mail(subject, message, sender, recipient_list=[email])
