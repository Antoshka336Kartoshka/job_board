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
    portfolio_link = models.URLField(null=True, blank=True)
    cv_file = models.FileField(upload_to='users/cv/', null=True, blank=True)
    user_photo = models.ImageField(upload_to='users/photo/', default='img/default_user_photo.png')
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'boarduser'


class Job(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    responsibility = models.TextField()
    qualifications = models.TextField()
    benefits = models.TextField()
    company_name = models.CharField(max_length=30)
    company_logo = models.ImageField(upload_to='users/companies_logos/', default='img/default_company_logo.png')
    published_date = models.DateField(auto_now_add=True)
    positions_number = models.PositiveSmallIntegerField(default=1)
    salary_from = models.PositiveIntegerField(blank=True, null=True)
    # Do validator for salary_from < salary_to
    salary_to = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=30)
    job_nature = models.CharField(max_length=15)
    created_by = models.ForeignKey(BoardUser, on_delete=models.CASCADE, related_name='created_by')
    responding_users = models.ManyToManyField(BoardUser, related_name='responding_users')

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
