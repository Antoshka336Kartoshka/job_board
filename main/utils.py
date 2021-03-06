from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


account_activation_token = AccountActivationTokenGenerator()


def is_employer(user) -> bool:
    return user.groups.filter(name='employer').exists()


def is_jobseeker(user) -> bool:
    return user.groups.filter(name='jobseeker').exists()


def capfirst(text: str) -> str:
    return text[0].upper() + text[1:]
