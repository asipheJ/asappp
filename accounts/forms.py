from django import forms
from .models import Account
from django.contrib.auth.forms import AuthenticationForm

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'id_number', 'username', 'password']

    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
