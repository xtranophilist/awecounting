from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.day_book, name='new_day_book'),
                       url(r'^(?P<id>[0-9]+)/$', views.day_book, name='view_day_book'),
                       url(r'^save/cash_sales/$', views.save_cash_sales, name='save_cash_sales'),
                       url(r'^save/day_cash_purchase/$', views.save_cash_purchase, name='save_cash_purchase'),
                       url(r'^save/cash_receipt/$', views.save_cash_receipt, name='save_cash_receipt'),
                       url(r'^save/cash_payment/$', views.save_cash_payment, name='save_cash_payment'),
                       # url(r'^day/save/(?P<submodel>[a-zA-Z0-9_.-]+)/$', views.save_submodel, name='save_submodel'),
                       )

