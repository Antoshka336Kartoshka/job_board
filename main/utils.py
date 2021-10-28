from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


account_activation_token = AccountActivationTokenGenerator()


def is_employer(user):
    return user.groups.filter(name='employer').exists()