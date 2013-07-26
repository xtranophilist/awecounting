from django.conf.urls import patterns, include, url
from registration.backends.default.views import RegistrationView
from users.forms import UserRegistrationForm
from users.views import web_login, logout

from rest_framework.urlpatterns import format_suffix_patterns
from users.views import UserList

urlpatterns = patterns('',
    url(r'^login/$', web_login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^register/$', RegistrationView.as_view(form_class=UserRegistrationForm, template_name='registration/registration_form.html')),
    url(r'^logout/$', logout, name='logout'),
    url(r'^list$', UserList.as_view(), name='user-list'),
    # url(r'^$', 'users.views.profile'),
    # url(r'^edit/$', 'users.views.edit_profile'),
    # url(r'^auth-error/$', 'users.views.auth_error'),
    (r'^', include('registration.backends.default.urls')),
    # url(r'^(?P<username>[a-zA-Z0-9_.-]+)/$', 'users.views.profile', name='user-detail'),
 )

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])