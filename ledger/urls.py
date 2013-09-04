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
                       url(r'^account/(?P<id>[0-9]+)/delete$', views.delete_account, name='delete_account'),

                       url(r'^party/create/$', views.party_form, name='create_party'),
                       url(r'^party/(?P<id>[0-9]+)/$', views.party_form, name='update_party'),

                       url(r'^categories/$', views.list_categories, name='list_category'),
                       url(r'^category/create$', views.create_category, name='create_category'),
                       url(r'^category/(?P<id>[0-9]+)/$', views.update_category, name='update_category'),
                       url(r'^category/(?P<id>[0-9]+)/delete$', views.delete_category, name='delete_category'),
)

