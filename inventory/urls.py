from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^items/$', views.list_all_items, name='list_all_items'),
                       url(r'^create/$', views.item_form, name='create_item'),
                       # url(r'^$', views.ListItem.as_view(template_name='list.html'), name='list_items'),
                       url(r'^items/json/$', views.items_as_json, name='items_as_json'),
                       url(r'^accounts/json/$', views.accounts_as_json, name='accounts_as_json'),
                       url(r'^accounts/(?P<day>\d{4}-\d{2}-\d{2}).json$', views.accounts_by_day_as_json,
                           name='accounts_by_day_as_json'),
                       url(r'^(?P<id>[0-9]+)/$', views.item_form, name='update_inventory_item'),
                       )

