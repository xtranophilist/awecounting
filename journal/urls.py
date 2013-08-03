from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^day/$', views.day_journal, name='new_day_journal'),
                       url(r'^day/(?P<id>[0-9]+)/$', views.day_journal, name='view_day_journal'),
                       )
