from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # url(r'^create/$', views.CreateAccount.as_view(template_name='create_form.html'), name='create_account'),
    url(r'^$', views.index, name='tax_schemes'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailAccount.as_view(template_name='detail.html'), name='detail_view'),
    )

