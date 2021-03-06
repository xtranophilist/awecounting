from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^items/$', views.list_all_items, name='list_all_items'),
                       url(r'^create/$', views.item_form, name='create_inventory_item'),
                       url(r'^item/delete/(?P<id>[0-9]+)$', views.delete_inventory_item, name='delete_inventory_item'),
                       url(r'^create_item/$', views.create_item, name='create_inventory_item_returning_account'),

                       url(r'^items/json/$', views.items_as_json, name='items_as_json'),
                       url(r'^accounts.json$', views.accounts_as_json, name='accounts_as_json'),
                       url(r'^accounts/(?P<day>\d{4}-\d{2}-\d{2}).json$', views.accounts_by_day_as_json,
                           name='accounts_by_day_as_json'),
                       url(r'^(?P<id>[0-9]+)/$', views.item_form, name='update_inventory_item'),

                       url(r'^categories/$', views.list_categories, name='list_inventory_category'),
                       url(r'^category/create/$', views.create_category, name='create_inventory_category'),
                       url(r'^category/(?P<id>[0-9]+)/$', views.update_category, name='update_inventory_category'),
                       url(r'^category/(?P<id>[0-9]+)/delete$', views.delete_category, name='delete_inventory_category'),

                       url(r'^units/$', views.list_units, name='list_units'),
                       url(r'^unit/create/$', views.unit_form, name='create_unit'),
                       url(r'^unit/(?P<id>[0-9]+)/$', views.unit_form, name='update_unit'),
                       url(r'^unit/(?P<id>[0-9]+)/delete$', views.delete_unit, name='delete_unit'),
)

