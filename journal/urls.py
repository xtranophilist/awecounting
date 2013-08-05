from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^day/$', views.day_journal, name='new_day_journal'),
                       url(r'^day/(?P<id>[0-9]+)/$', views.day_journal, name='view_day_journal'),
                       url(r'^day/save/day_cash_sales/$', views.save_day_cash_sales, name='save_day_cash_sales'),
                       url(r'^day/save/day_cash_purchase/$', views.save_day_cash_purchase, name='save_day_cash_purchase'),
                       # url(r'^day/save/(?P<submodel>[a-zA-Z0-9_.-]+)/$', views.save_submodel, name='save_submodel'),
                       )

