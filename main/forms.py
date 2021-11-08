from django.forms import ModelForm, ValidationError, Textarea
from django.forms.fields import CharField, EmailField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from main.models import BoardUser, Job, Company
from main.utils import capfirst


class RegistrationForm(UserCreationForm):
    username = CharField(min_length=3, max_length=30)
    first_name = CharField(min_length=2, max_length=20)
    last_name = CharField(min_length=2, max_length=20)
    email = EmailField()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return capfirst(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return capfirst(last_name)

    class Meta:
        model = BoardUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login':
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive.",
        'inactive': "This account is not activated. Please confirm your email to activate it",
    }

    def get_invalid_login_error(self):

        user = self.get_user()

        if user and not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive', )
        else:
            return ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )

    class Meta:
        model = BoardUser


class AccountSettingsForm(ModelForm):
    first_name = CharField(min_length=2, max_length=20)
    last_name = CharField(min_length=2, max_length=20)
    speciality = CharField(min_length=3, max_length=30, required=False)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return capfirst(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return capfirst(last_name)

    class Meta:
        model = BoardUser
        fields = ['first_name', 'last_name', 'speciality', 'portfolio_link', 'cv_file', 'user_photo', 'company']


class CompanyForm(ModelForm):

    def clean_name(self):
        name = self.cleaned_data['name']
        return capfirst(name)

    class Meta:
        model = Company
        fields = ['name', 'company_logo']


class JobForm(ModelForm):
    name = CharField(min_length=3, max_length=30)
    description = CharField(min_length=10, widget=Textarea)
    responsibility = CharField(min_length=10, widget=Textarea)
    qualifications = CharField(min_length=10, widget=Textarea)
    benefits = CharField(min_length=10, widget=Textarea)
    location = CharField(min_length=3, max_length=30)

    def clean_name(self):
        name = self.cleaned_data['name']
        return capfirst(name)

    def clean_company_name(self):
        company_name = self.cleaned_data['company_name']
        return capfirst(company_name)

    def clean(self):  # Salary validation
        super().clean()
        errors = {}
        if self.cleaned_data['salary_from'] and self.cleaned_data['salary_to']:
            if self.cleaned_data['salary_from'] > self.cleaned_data['salary_to']:
                errors['salary_to'] = ValidationError('Salary from more than salary to')
        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Job
        exclude = ['created_by', 'responding_users', 'published_date']
