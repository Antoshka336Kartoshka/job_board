from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.fields import CharField, EmailField
from main.models import BoardUser, Job
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        model = BoardUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        field_classes = {'username': CharField,
                         'first_name': CharField,
                         'last_name': CharField,
                         'email': EmailField}


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
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive', )
        else:
            return forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )

    class Meta:
        model = BoardUser


class AccountSettingsForm(ModelForm):

    class Meta:
        model = BoardUser
        fields = ['first_name', 'last_name', 'speciality', 'portfolio_link', 'cv_file', 'user_photo']


class JobForm(ModelForm):

    class Meta:
        model = Job
        exclude = ['created_by', 'responding_users', 'published_date']