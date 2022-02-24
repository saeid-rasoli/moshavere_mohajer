from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import UserSignupForm, EmployeeForm


def index(request):
    return render(request, 'index.html', {})


def signup(request):
    success_message = 'ثبت نام با موفقیت صورت گرفت'
    if request.method == 'POST':
        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('moshavere:login')
    else:
        form = UserSignupForm()
    context = {
        'form': form
    }
    return render(request, 'auth/signup.html', context)


def login(request):
    return render(request, 'auth/login.html', {})


def employee(request):
    success_message = 'اطاعات شما ثبت شد'
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST or None)
        if form.is_valid():
            user = request.user
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('moshavere:index')
    else:
        form = EmployeeForm()
    context = {
        'form': form
    }
    return render(request, 'profile/employee.html', context)
