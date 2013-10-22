from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^accounts/json/$', views.accounts_as_json, name='accounts_as_json'),
                       url(r'^$', views.list_accounts, name='list_account'),
                       url(r'^create/$', views.account_form, name='create_account'),
                       url(r'^(?P<id>[0-9]+)/update/$', views.account_form, name='update_account'),
                       url(r'^accounts/(?P<day>\d{4}-\d{2}-\d{2}).json$', views.accounts_by_day_as_json,
                           name='accounts_by_day_as_json'),
                       url(r'^(?P<id>[0-9]+)/$', views.view_account, name='view_account'),
                       url(r'^account/(?P<id>[0-9]+)/delete/$', views.delete_account, name='delete_account'),

                       url(r'^parties/$', views.list_all_parties, name='list_all_parties'),
                       url(r'^party/create/$', views.party_form, name='create_party'),
                       url(r'^party/(?P<id>[0-9]+)/$', views.party_form, name='update_party'),
                       url(r'^party/(?P<id>[0-9]+)/delete$', views.delete_party, name='delete_party'),
                       url(r'^party/customers.json$', views.customers_as_json, name='customers_as_json'),
                       url(r'^party/suppliers.json$', views.suppliers_as_json, name='suppliers_as_json'),

                       url(r'^categories/$', views.list_categories, name='list_category'),
                       url(r'^category/create/$', views.create_category, name='create_category'),
                       url(r'^category/(?P<id>[0-9]+)/$', views.update_category, name='update_category'),
                       url(r'^category/(?P<id>[0-9]+)/delete$', views.delete_category, name='delete_category'),
)
