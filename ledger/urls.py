from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       # url(r'^create/$', views.CreateAccount.as_view(template_name='create_form.html'), name='create_account'),
                       url(r'^accounts/json/$', views.accounts_as_json, name='accounts_as_json'),
                       # url(r'^$', views.ListAccount.as_view(template_name='list.html'), name='list_account'),
                       # url(r'^(?P<pk>[0-9]+)/$', views.DetailAccount.as_view(template_name='detail.html'), name='detail_view'),
                       url(r'^$', views.list_accounts, name='list_account'),
                       url(r'^create/$', views.account_form, name='create_account'),
                       url(r'^(?P<id>[0-9]+)/update/$', views.account_form, name='update_account'),
                       url(r'^accounts/(?P<day>\d{4}-\d{2}-\d{2}).json$', views.accounts_by_day_as_json,
                           name='accounts_by_day_as_json'),
                       url(r'^(?P<id>[0-9]+)/$', views.view_account, name='view_account'),
)

