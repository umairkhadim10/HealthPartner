from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ItemsModelFormset
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.hashers import check_password
from .tables import ItemsTable
from django.core.paginator import Paginator
from .decorators import login_register_check
import tweepy
import requests
# from facebook_posts.models import Post
import praw
from .task import get_post_by_reddit_Api
from django_celery_beat.models import PeriodicTask, IntervalSchedule


# Create your views here.

@login_register_check
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


@login_register_check
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

    # schedule, created = IntervalSchedule.objects.get_or_create(
    #     every=10,
    #     period=IntervalSchedule.SECONDS,
    # )
    # PeriodicTask.objects.create(
    #     interval=schedule,  # we created this above.
    #     name='Importing reddits from',  # simply describes this periodic task.
    #     task='customer.task.get_post_by_reddit_Api',  # name of task.
    # )

    items_submission = ItemSubmissionDate.objects.filter(customer=request.user).order_by('-create_date')[:5]
    sub_reddit = Tweets.objects.all()[:5]
    context = {
        'sub_reddit': sub_reddit,
        "table": items_submission,

    }
    return render(request, 'customer/dashboard.html', context)


# function to compute the calories of a customer for a day

@login_required(login_url='login')
def customer_calorie_compute(request):
    if ItemSubmissionDate.objects.filter(create_date=date.today(), customer=request.user).exists():
        return redirect('dashboard')

    formset = ItemsModelFormset(queryset=Items.objects.none())
    if request.method == 'POST':
        formset = ItemsModelFormset(request.POST, )
        if formset.is_valid():
            item_submission_date = ItemSubmissionDate(create_date=date.today(), customer=request.user)
            item_submission_date.save()
            for form in formset:

                if form.cleaned_data.get('name'):
                    item = form.save(commit=False)
                    item.item_submissions_date = item_submission_date
                    item.save()

    print(formset.errors)
    context = {
        'formset': formset
    }

    return render(request, 'customer/compute_calories.html', context)


@login_required(login_url='login')
def customer_calorie_view(request):
    sort = request.GET.get('sort')
    if sort:
        if sort == 'calories':
            if request.GET.get('dir') == 'asc':
                items_submission = sorted(ItemSubmissionDate.objects.filter(customer=request.user),
                                          key=lambda m: m.calories)

            elif request.GET.get('dir') == 'desc':
                items_submission = sorted(ItemSubmissionDate.objects.filter(customer=request.user),
                                          key=lambda m: m.calories, reverse=True)

        elif sort == 'create_date':
            if request.GET.get('dir') == 'asc':
                items_submission = ItemSubmissionDate.objects.filter(customer=request.user).order_by('create_date')

            elif request.GET.get('dir') == 'desc':
                items_submission = ItemSubmissionDate.objects.filter(customer=request.user).order_by('-create_date')

    else:
        items_submission = ItemSubmissionDate.objects.filter(customer=request.user)
    paginator = Paginator(items_submission, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "table": page_obj,

    }
    return render(request, 'customer/view_calorie_submission.html', context)
