from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from _class.models import Classroom

def basic_vars(request):
    user = User.objects.filter(username=request.user.username).first()
    classes = []
    for i in Classroom.objects.all():
        if user in i.teachers.all() or user in i.students.all():
            classes.append(i)

    return user, classes

def home(request):
    user, classes = basic_vars(request)

    context = {
        'user': user,
        'classes': classes,
    }
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if request.POST.get('next', ''):
                return redirect(f"{request.POST.get('next', '')}")
            return redirect('/')
        else:
            # No backend authenticated the credentials
            messages.error(request, 'Bad credentials', 'alert-danger')
            if request.POST.get('next', ''):
                return redirect(f"/accounts/login/?next={request.POST.get('next', '')}")
            return redirect('/accounts/login/')

    context = {}
    if request.user.is_authenticated:
        context = {'account_change': True}

    return render(request, 'login.html', context)

def sign_up(request):
    if request.method == 'POST':
        messages.info(request, 'Please login to verify it was you', 'alert-primary')
        return redirect('/accounts/login/')

    context = {}
    if request.user.is_authenticated:
        context = {'account_change': True}

    return render(request, 'sign_up.html', context)