from datetime import date, timedelta
from celery import shared_task
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from main.models import BoardUser

from main.utils import account_activation_token


@shared_task
def send_registration_email(user_pk, domain):
    """
    Send registration email to user
    """
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


@shared_task
def remove_inactive_users():
    """
    Remove users wich accounts was not activated more than a week ago once a week
    """
    week_ago_date = date.today() - timedelta(days=7)
    inactive_users = BoardUser.objects.filter(
        is_active=False, date_joined__lte=week_ago_date)
    inactive_users_count = len(inactive_users)
    inactive_users.delete()
    return f'{inactive_users_count} inactive users was deleted.'
