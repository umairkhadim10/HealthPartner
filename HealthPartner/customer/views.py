from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.hashers import check_password
from .tables import ItemsTable
from django.core.paginator import Paginator


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
    items_submission = ItemSubmissionDate.objects.filter(customer=request.user).order_by('-id')[:5]
    paginator = Paginator(items_submission, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tweets = Tweets.objects.all()[:5]
    # last_five_items = Items.objects.all().order_by('item_submissions_date')[:5]
    context = {
        'tweets': tweets,
        "table": page_obj
    }
    return render(request, 'customer/dashboard.html', context)


# function to compute the calories of a customer for a day

@login_required(login_url='login')
def customer_calorie_compute(request):
    if ItemSubmissionDate.objects.filter(create_date=date.today(), customer=request.user).exists():
        return redirect('dashboard')
    error = False
    if request.method == "POST":
        quantity_list = request.POST.getlist('quantity')
        food_list = request.POST.getlist('food_name')
        for quantity in quantity_list:
            if int(quantity) < 1:
                messages.error(request, "Quantity cannot be less than 1 grams")
                error = True
        dic = {'food_list': food_list,
               'quantity_list': quantity_list,
               }
        if not error:
            item_submission_date = ItemSubmissionDate(create_date=date.today(), customer=request.user)
            item_submission_date.save()
            for i in range(len(dic['food_list'])):
                item = Items(name=dic['food_list'][i], quantity=dic['quantity_list'][i],
                             item_submissions_date=item_submission_date)
                item.save()

    return render(request, 'customer/compute_calories.html', )


@login_required(login_url='login')
def customer_calorie_view(request):
    items_submission = ItemSubmissionDate.objects.filter(customer=request.user)
    paginator = Paginator(items_submission, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "table": page_obj
    }
    return render(request, 'customer/view_calorie_submission.html', context)
