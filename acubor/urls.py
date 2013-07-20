from django.conf.urls import patterns, url, include
from users import views
# from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # ('^$', TemplateView.as_view(template_name='site_index.html')),
    url(r'^$', views.index, name='index'),
    (r'^user/', include('users.urls')),
    (r'^user/', include('users.urls')),
    (r'^voucher/', include('voucher.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    )
