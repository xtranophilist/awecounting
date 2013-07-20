from django.shortcuts import render, redirect
from users.forms import UserRegistrationForm
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout


def index(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard_index.html')
    return render(request, 'site_index.html', {"registration_form": UserRegistrationForm})


def web_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, **kwargs)


def logout(request, next_page=None):
    auth_logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('/')
