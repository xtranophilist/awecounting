from django.conf.urls import patterns, url, include
from users import views
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
# router.register(r'groups', GroupViewSet)

urlpatterns = patterns('',
    # ('^$', TemplateView.as_view(template_name='site_index.html')),
    url(r'^$', views.index, name='home'),
    (r'^user/', include('users.urls')),
    (r'^user/', include('users.urls')),
    (r'^voucher/', include('voucher.urls')),
    (r'^account/', include('ledger.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    )
