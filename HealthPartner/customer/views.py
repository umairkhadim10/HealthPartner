from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password


# Create your views here.


def customer_signup(request):
    signup_form = SignUpForm()
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('login')
    context = {
        'form': signup_form
    }
    return render(request, 'customer/signup.html', context)


def customer_login(request):
    login_form = LoginForm()
    if request.method == "POST":
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')
        user = authenticate(username=user_name, password=user_password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "incorrect username or password")

    context = {
        'form': login_form
    }
    return render(request, 'customer/login.html', context)


@login_required(login_url='login')
def customer_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def customer_dashboard(request):
    tweets = Tweets.objects.all()
    last_five_items = Items.objects.all().order_by('-item_submissions')[:5]
    context = {
        'tweets': tweets,
        "Last_five_submissions": last_five_items
    }
    return render(request, 'customer/dashboard.html', context)


# function to compute the calories of a customer for a day


def customer_calorie_compute(request):
    tweets = Tweets.objects.all()
    last_five_items = Items.objects.all().order_by('-item_submissions')[:5]
    context = {
        'tweets': tweets,
        "Last_five_submissions": last_five_items
    }
    return render(request, 'customer/compute_calories.html', context)