from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms.fields import CharField, EmailField
from django.utils.translation import gettext_lazy as _
from main.models import BoardUser
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

        user = BoardUser.objects.get(username=self.cleaned_data.get('username'))

        if not user.is_active and user:
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


class AccountSettingsForm(UserChangeForm):

    class Meta:
        model = BoardUser
        fields = ['first_name', 'last_name', 'email', 'portfolio_link', 'cv_file', 'user_photo', 'company']
