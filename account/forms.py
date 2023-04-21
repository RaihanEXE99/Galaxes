from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=15, help_text='Required', widget=forms.TextInput(attrs={
        "class" : "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
        "type" : "text",
        "placeholder" : ""
    }))
    email = forms.CharField(max_length=30, help_text='Required', widget=forms.TextInput(attrs={
        "class" : "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
        "type" : "text",
        "placeholder" : ""
    }))
    password = forms.CharField(max_length=30, help_text='Required', widget=forms.TextInput(attrs={
        "class" : "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
        "type" : "password",
        "placeholder" : ""
    }))
    class Meta:
        model = Account
        fields = ('username', 'email','password', )
