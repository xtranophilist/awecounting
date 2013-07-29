from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^invoice/$', views.invoice, name='invoice'),
    url(r'^invoice/save/$', views.save_invoice, name='save_invoice')
    )
