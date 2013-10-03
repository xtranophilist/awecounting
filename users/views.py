from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import generics

from users.forms import UserRegistrationForm
from users.serializers import UserSerializer


def index(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard_index.html')
    return render(request, 'site_index.html', {"registration_form": UserRegistrationForm})


def web_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        if request.method == 'POST':
            if request.POST.has_key('remember_me'):
                request.session.set_expiry(1209600) # 2 weeks
            else:
                request.session.set_expiry(0)
        return login(request, **kwargs)


def logout(request, next_page=None):
    auth_logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('/')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListCreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer


#def role_management(request):
    #roles = Role.objects.get(company=)