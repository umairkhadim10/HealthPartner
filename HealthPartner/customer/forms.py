from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class ComputeCaloriesForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['name', 'quantity']