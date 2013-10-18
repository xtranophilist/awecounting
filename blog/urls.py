from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
                       url(r'^$', views.list_blog_entries, name='list_blog_entries'),
                       url(r'^author/(?P<username>[a-z0-9_]+)/$', views.view_blogs_by_author, name='view_blogs_by_author'),
                       url(r'^(?P<id>[0-9]+)/$', views.view_blog_entry, name='view_blog_entry'),
)