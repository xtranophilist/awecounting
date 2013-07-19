from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # url(r'^login/$', web_login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^sales/$', views.sales, name='sales-voucher'),
    # url(r'^$', views.index, name='index')
    )
