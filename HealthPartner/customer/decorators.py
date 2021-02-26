from django.shortcuts import redirect


def login_register_check(view_func):
    def is_logged_in(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return is_logged_in
