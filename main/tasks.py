from celery import shared_task
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from main.models import BoardUser

from main.utils import account_activation_token


@shared_task
def send_registration_email(user_pk, domain):
    user = BoardUser.objects.get(pk=user_pk)
    mail_subject = 'Activation link from Job Board'
    message = render_to_string('main/account/email_confirmation.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return f'Registration email was sent to {user.email}'
