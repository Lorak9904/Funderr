from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=30, label='First Name')
    last_name = forms.CharField(required=True, max_length=30, label='Last Name')
    email = forms.EmailField()
    # company = forms.CharField(max_length=100)
    

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
    
        

