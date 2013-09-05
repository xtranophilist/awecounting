from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^entry/$', views.entry, name='create_payroll_entry'),
                       url(r'^entries/$', views.list_payroll_entries, name='list_payroll_entries'),
                       url(r'^(?P<id>[0-9]+)/$', views.entry, name='update_payroll_entry'),
                       url(r'^entry/delete/(?P<id>[0-9]+)/$', views.delete_payroll_entry, name='delete_payroll_entry'),

                       url(r'^save/$', views.save_entry, name='save_payroll_entry'),
)
