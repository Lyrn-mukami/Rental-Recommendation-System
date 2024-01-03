from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Username'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'Repeat password'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Email'}))
class LoginForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'Password'}))
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']