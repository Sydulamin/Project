# Create your views here.
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render

from .models import *


def index(request):
    return render(request, 'index.html', locals())


def registration(request):
    if request.user.is_active:
        return redirect('/')
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'This username is already taken, try another')
                return redirect('registration')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'This email is already taken, try another')
                return redirect('registration')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.set_password(password)
                user.save()
                messages.success(request, 'Profile created, login now')
                return redirect('login')
        else:
            messages.warning(request, 'Miss match password')
            return redirect('registration')
    else:
        return render(request, 'registration.html', locals())


def login(request):
    if request.user.is_active:
        return redirect('/')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_active and user.is_staff:
                return redirect('member')
            else:
                return redirect('profile')
        else:
            messages.error(request, 'User not found, create an account')
            return redirect('registration')
    else:
        return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return redirect('index')


def profile(request):
    return render(request, 'profile.html', locals())


def member(request):
    return render(request, 'member.html', locals())
