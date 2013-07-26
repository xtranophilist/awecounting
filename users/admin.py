from django.contrib import admin
from models import User, Company
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

admin.site.register(User)
admin.site.register(Company)
admin.site.unregister(Site)

admin.site.unregister(Group)
admin.site.register(Group)