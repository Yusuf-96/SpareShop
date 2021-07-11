from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, authenticate
from django.contrib.auth.models import User, auth

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            return redirect('login')
    return render(request, 'accounts/login.html')