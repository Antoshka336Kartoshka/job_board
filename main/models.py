from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


# Create your models here.


class BoardUser(AbstractUser):  # Модель посльзователя
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=30,
        unique=True,
        help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': ["A user with that username already exists."]},
        default=None)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, help_text='Designates whether this user '
                                                             'should be treated as active.')
    company_name = models.CharField(max_length=50)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'boarduser'
