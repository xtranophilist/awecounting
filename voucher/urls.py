from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^sales/$', views.sales, name='sales-voucher'),
    )
