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
    items_submission = ItemSubmissionDate.objects.filter(customer=request.user)
    paginator = Paginator(items_submission, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tweets = Tweets.objects.all()
    # last_five_items = Items.objects.all().order_by('item_submissions_date')[:5]
    context = {
        'tweets': tweets,
        "table": page_obj
    }
    return render(request, 'customer/dashboard.html', context)


# function to compute the calories of a customer for a day

@login_required(login_url='login')
def customer_calorie_compute(request):
    item_formset = modelformset_factory(Items, fields=('name', 'quantity',), extra=10)
    # item_formset = inlineformset_factory(ItemSubmissionDate, Items, fields=('name', 'quantity',))
    formset = item_formset()

    if request.method == "POST":
        formset = item_formset(request.POST)
        if formset.is_valid():
            # formset.save(commit=False)
            # formset.customer = request.user
            if ItemSubmissionDate.objects.filter(create_date=date.today(), customer=request.user).exists():
                return redirect('dashboard')
            item_submission_date = ItemSubmissionDate(create_date=date.today(), customer=request.user)
            item_submission_date.save()
            formsets = formset.save(commit=False)
            for form in formsets:
                form.item_submissions_date = item_submission_date
                form.save()

    context = {
        'form': formset
    }

    return render(request, 'customer/compute_calories.html', context)


@login_required(login_url='login')
def customer_calorie_view(request):
    items_submission = ItemSubmissionDate.objects.filter(customer=request.user)
    print(items_submission)
    paginator = Paginator(items_submission, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    context = {
        "table": page_obj
    }
    return render(request, 'customer/view_calorie_submission.html', context)
