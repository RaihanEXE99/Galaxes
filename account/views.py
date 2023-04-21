from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from .models import Account,MyAccountManager
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.hashers import make_password

# from gameLogics.models import GameAccount
# from gameLogics import views

def registration_view(request):
    if request.method == "POST":
        password = request.POST['password']
        username = request.POST['username']
        email = request.POST['email']
        if (password == "") or len(password)<6 or username == "" or email == "":
            if (password == ""):
                messages.error(request, 'password Field is empty!')    
            if len(password)<6:
                messages.error(request, 'weak password (less than 6 alphabets)!')   
            if username == "":
                messages.error(request, 'username Field is empty!')  
            if email == "":
                messages.error(request, 'email Field is empty!') 
        else:
            try:
                password = make_password(password)
                acc = Account(username=username, email=email, password=password)
                acc.save()
                return redirect('account:signIn_view')
            except:
                messages.error(request, "Username is taken or something wrong happened!Try Again")
    return render(request, 'account/register.html')

def signIn_view(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('gameLogics:mainGameDashboard')
            else:
                messages.error(request, "Something wrong happened \_(-_-)_/")
        except:
            messages.error(request, "Something wrong happened \_(-_-)_/")
    return render(request, 'account/signIn.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def home_view(request):
    if request.user.is_authenticated:
        return redirect("gameLogics:mainGameDashboard")
    return render(request, 'account/home.html')

def sampleFuture(request,title):
    return render(request, 'account/sample/sampleFuture.html',{
        "title":title
    })