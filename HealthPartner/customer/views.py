from datetime import date

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ItemsModelFormset
from django.core.paginator import Paginator
from .decorators import login_register_check
from django.core.mail import EmailMessage
# Function for customer signup
from .tokens import account_activation_token


@login_register_check
def customer_signup(request):
    signup_form = SignUpForm()
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            # return redirect('login')

            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your HealthPartner account.'
            message = render_to_string('customer/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = signup_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'customer/account_confirmation_message.html',)

    context = {
        'form': signup_form
    }
    return render(request, 'customer/signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request, 'customer/account_confirmation.html',)
    else:
        return HttpResponse('Activation link is invalid!')


# Function for customer login

@login_register_check
def customer_login(request):
    login_form = LoginForm()
    if request.method == "POST":
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')
        user = authenticate(username=user_name, password=user_password)
        if user is not None:
            user_confirmation = User.objects.get(username=user_name)
            if user_confirmation.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Please verify your account !!")
        else:
            messages.error(request, "incorrect Username or Password")

    context = {
        'form': login_form
    }
    return render(request, 'customer/login.html', context)


# Function for customer logout

@login_required(login_url='login')
def customer_logout(request):
    logout(request)
    return redirect('login')


# Function for getting subreddits and customer calories and pass to template

@login_required(login_url='login')
def customer_dashboard(request):
    # reddit = praw.Reddit(client_id='ISnOA13qK99q4A',
    #                      client_secret='cEKVwb65zJJoejN6YphDRamyHycdHA',
    #                      user_agent='my user agent')
    #
    # # to find the top most submission in the subreddit "HEALTH"
    # subreddit = reddit.subreddit('HEALTH')

    # for submission in subreddit.top(limit=5):
    #
    #     dt = datetime.datetime.fromtimestamp(float(submission.created_utc))
    #     print(dt)
    #     tweets = Tweets(create_time=dt, description=submission.title)
    #     tweets.save()
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
    # block customer submission if he has already submitted today's meals detail
    if ItemSubmissionDate.objects.filter(create_date=date.today(), customer=request.user).exists():
        return render(request, 'customer/compute_calories_denied.html')

    # creating multiple forms for Customer items submissions
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

    context = {
        'formset': formset
    }

    return render(request, 'customer/compute_calories.html', context)


# Function to show Customer Calorie View having pagination and sort Columns as per of Customer request


@login_required(login_url='login')
def customer_calorie_view(request):
    # check if the user request for sorting or not
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

    # paginate the items_submission list
    paginator = Paginator(items_submission, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "table": page_obj,

    }
    return render(request, 'customer/view_calorie_submission.html', context)
