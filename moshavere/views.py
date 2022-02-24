from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def signup(request):
    return render(request, 'auth/signup.html', {})

def login(request):
    return render(request, 'auth/login.html', {})