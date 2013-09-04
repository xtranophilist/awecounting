from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # url(r'^create/$', views.CreateAccount.as_view(template_name='create_form.html'), name='create_account'),
    url(r'^schemes/$', views.list_tax_schemes, name='list_tax_schemes'),
    url(r'^scheme/create$', views.tax_scheme_form, name='create_tax_schemes'),
    url(r'^scheme/(?P<id>[0-9]+)$', views.tax_scheme_form, name='update_tax_schemes'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailAccount.as_view(template_name='detail.html'), name='detail_view'),
    url(r'^schemes/json/$', views.schemes_as_json, name='tax_schemes_as_json'),
    )

