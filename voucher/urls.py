from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^invoice/$', views.invoice, name='invoice'),
    )
