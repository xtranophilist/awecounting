from django.shortcuts import render
from users.forms import UserRegistrationForm


def index(request):

    return render(request, 'site_index.html', {"form": UserRegistrationForm})
