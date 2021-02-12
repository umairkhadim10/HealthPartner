from django.shortcuts import render
from .forms import *

# Create your views here.


def signup(request):
    signup_form = SignUpForm()
    if request.method == "POST":
        signup_form=SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
    context = {
        'form': signup_form
    }
    return render(request, 'customer/signup.html', context)