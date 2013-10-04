from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import generics
from django.contrib import messages
from django.contrib.auth.models import Group

from users.forms import UserRegistrationForm
from users.serializers import UserSerializer
from users.models import Company, Role, User


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


def user_setting(request):
    if request.POST:
        request.user.full_name = request.POST['full_name']
        request.user.email = request.POST['email']
        request.user.save()
    return render(request, 'user_setting.html')


def set_company(request, id):
    company = Company.objects.get(id=id)
    request.session['company'] = company.id
    return redirect(request.META.get('HTTP_REFERER', None))


@login_required
def roles(request):
    if request.POST:
        print request.POST
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(request.POST['user'])
            try:
                user = User.objects.get(email=request.POST['user'])
                group = Group.objects.get(name=request.POST['group'])
                try:
                    Role.objects.get(user=user, company=request.company, group=group)
                    messages.error(request,
                                   'User ' + user.username + ' (' + user.email + ') is already the ' + request.POST[
                                       'group'] + '.')
                except Role.DoesNotExist:
                    role = Role(user=user, company=request.company, group=group)
                    role.save()
                    messages.success(request,
                                     'User ' + user.username + ' (' + user.email + ') added as ' + request.POST[
                                         'group'] + '.')
            except User.DoesNotExist:
                messages.error(request, 'No users found with the e-mail address ' + request.POST['user'])
        except ValidationError:
            try:
                user = User.objects.get(username=request.POST['user'])
                group = Group.objects.get(name=request.POST['group'])
                try:
                    Role.objects.get(user=user, company=request.company, group=group)
                    messages.error(request,
                                   'User ' + user.username + ' (' + user.email + ') is already the ' + request.POST[
                                       'group'] + '.')
                except Role.DoesNotExist:
                    role = Role(user=user, company=request.company, group=group)
                    role.save()
                    messages.success(request,
                                     'User ' + user.username + ' (' + user.email + ') added as ' + request.POST[
                                         'group'] + '.')
            except User.DoesNotExist:
                messages.error(request, 'No users found with the username ' + request.POST['user'])
    objs = Role.objects.filter(company=request.company)
    return render(request, 'roles.html', {'roles': objs})


def delete_role(request, id):
    obj = Role.objects.get(company=request.company, id=id)
    if not obj.group.name == 'SuperOwner':
        obj.delete()
    return redirect(reverse('roles'))