from django.conf.urls import patterns, url, include
from users import views as users_views
from core import views as core_views
# from django.views.generic import TemplateView
from rest_framework import viewsets, routers
from django.contrib.auth import get_user_model


from django.contrib import admin
admin.autodiscover()

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = get_user_model()

# class GroupViewSet(viewsets.ModelViewSet):
#     model = Group

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = patterns('',

                       url(r'^$', users_views.index, name='home'),
                       (r'^user/', include('users.urls')),
                       (r'^user/', include('users.urls')),
                       (r'^voucher/', include('voucher.urls')),
                       (r'^account/', include('ledger.urls')),
                       (r'^tax/', include('tax.urls')),
                       (r'^inventory/', include('inventory.urls')),
                       (r'^journal/', include('daybook.urls')),
                       (r'^ledger/', include('ledger.urls')),

                       url(r'^settings/company/$', core_views.company_settings, name='company_settings'),
                       url(r'^party/create/$', core_views.party_form, name='create_party'),
                       url(r'^party/(?P<id>[0-9]+)/$', core_views.party_form, name='update_party'),

                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^', include(router.urls)),
                       url(r'^acubor-admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^acubor-admin/', include(admin.site.urls)),
                       )
