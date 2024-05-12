from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from functools import wraps
from .models import User
from django.http import HttpResponseBadRequest

def login(request):
    return render(request,'login.html')

def logout(request):
    django_logout(request)
    request.session.set_expiry(0)  
    return redirect('/login/')
def exit(request):
    access_token = request.session.get('access_token')
    if access_token :
        user = User.objects.get(token_access=access_token)
        user.is_available = False
        user.save()
    return redirect('/game/')

def game(request):
    access_token = request.session.get('access_token')
    if access_token is None:
        return redirect('/')
    if access_token:
        try:
            user = User.objects.get(token_access=access_token)
            users = User.objects.exclude(token_access=access_token)
        except User.DoesNotExist:
            return redirect('/')
    return render(request, 'game.html', {'login': user , 'users': users})


def profile(request):
    access_token = request.session.get('access_token')
    if access_token is None:
        return redirect('/')
    if access_token:
        try:
            user = User.objects.get(token_access=access_token)
        except User.DoesNotExist:
            return redirect('/')
    return render(request, 'profile.html', {'user': user})