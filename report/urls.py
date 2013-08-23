from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^trial-balance/$', views.trial_balance, name='trial_balance'),
    )

