from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^new$', views.entry, name='new_payroll'),
                       url(r'^(?P<id>[0-9]+)/$', views.entry, name='view_payroll'),
                       url(r'^save/$', views.save_entry, name='save_invoice'),
                       )
