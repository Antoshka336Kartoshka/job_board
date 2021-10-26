from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import CharField, EmailField
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
