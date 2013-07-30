from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # url(r'^create/$', views.CreateAccount.as_view(template_name='create_form.html'), name='create_account'),
    # url(r'^$', views.index, name='inventory_items'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailAccount.as_view(template_name='detail.html'), name='detail_view'),
    url(r'^create/$', views.item_form, name='create_item'),
    # url(r'^$', views.ListItem.as_view(template_name='list.html'), name='list_items'),
    url(r'^items/json/$', views.items_as_json, name='items_as_json'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailItem.as_view(template_name='detail.html'), name='detail_item'),
    )

