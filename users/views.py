from django.shortcuts import render, redirect
from users.forms import UserRegistrationForm
from django.contrib.auth.views import login


def index(request):
    return render(request, 'site_index.html', {"registration_form": UserRegistrationForm})


def web_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, **kwargs)
