from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
        # widgets = {
        #     'username': forms.TextInput(attrs={'placeholder': 'Name'}),
        #     'password': forms.TextInput(
        #         attrs={'placeholder': 'Password'}),
        # }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['name', 'quantity', ]