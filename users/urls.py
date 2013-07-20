from django.conf.urls import patterns, include, url
from registration.backends.default.views import RegistrationView
from users.forms import UserRegistrationForm
from users.views import web_login, logout

urlpatterns = patterns('',
    url(r'^login/$', web_login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^register/$', RegistrationView.as_view(form_class=UserRegistrationForm, template_name='registration/registration_form.html')),
    url(r'^logout/$', logout, name='logout'),
    # url(r'^$', 'users.views.profile'),
    # url(r'^edit/$', 'users.views.edit_profile'),
    # url(r'^auth-error/$', 'users.views.auth_error'),
    (r'^', include('registration.backends.default.urls')),
    # url(r'^(?P<username>[a-zA-Z0-9_.-]+)/$', 'users.views.profile', name='user-detail'),

 # url(r'^register/$', users_views.register_user, name='register'),
 )
