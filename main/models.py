from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


# Create your models here.


class BoardUser(AbstractUser):  # Модель посльзователя
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, help_text='Designates whether this user '
                                                            'should be treated as active.')
    portfolio_link = models.URLField(null=True, blank=True)
    cv_file = models.FileField(upload_to='users/cv/', null=True, blank=True)
    user_photo = models.ImageField(upload_to='users/photo/', default='img/default_user_photo.png')
    speciality = models.CharField(max_length=30, default='Specialty is not specified')
    company = models.OneToOneField('Company', on_delete=models.SET_NULL, null=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'boarduser'


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Company(models.Model):
    name = models.CharField(max_length=40)
    company_logo = models.ImageField(upload_to='users/companies_logos/', default='img/default_company_logo.png')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Job(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    responsibility = models.TextField()
    qualifications = models.TextField()
    benefits = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    positions_number = models.PositiveSmallIntegerField(default=1)
    salary_from = models.PositiveSmallIntegerField(blank=True, null=True)
    salary_to = models.PositiveSmallIntegerField(blank=True, null=True,
                                                 help_text='leave from and to fields empty to contractual salary')
    location = models.CharField(max_length=30)
    job_nature = models.CharField(max_length=15)
    created_by = models.ForeignKey(BoardUser, on_delete=models.CASCADE, related_name='created_by')
    responding_users = models.ManyToManyField(BoardUser, related_name='applied_jobs')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('job_details', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
