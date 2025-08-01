from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import RegisterForm, LoginForm, CreateUserForm

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

def register(request):
    form = CreateUserForm()     
        
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + user)
            return redirect('accounts:login')

    return render(request, 'accounts/register.html', {'form': form})  
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('public:index')
        else:
            messages.info(request, 'Username or Password Incorrect')
    context = {}
    return render(request, 'accounts/login.html',context)
def logout_user(request):
    logout(request)
    return redirect('public:index')