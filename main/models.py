from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=50)

    def __repr__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Company'


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
    portfolio_link = models.URLField(null=True, blank=True)
    cv_file = models.FileField(upload_to='cv', null=True, blank=True)
    user_photo = models.ImageField(upload_to='photo', null=True, blank=True)
    company = models.OneToOneField(Company, on_delete=models.SET_NULL, null=True, blank=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'boarduser'



