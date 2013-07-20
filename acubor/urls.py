from django.conf.urls import patterns, url, include
from users import views
# from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # ('^$', TemplateView.as_view(template_name='site_index.html')),
    url(r'^$', views.index, name='index'),
    (r'^user/', include('users.urls')),
    (r'^user/', include('users.urls')),
    (r'^voucher/', include('voucher.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    )
