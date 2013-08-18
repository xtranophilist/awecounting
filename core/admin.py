from django.contrib import admin
from models import Currency, CompanySetting, Tag

admin.site.register(Tag)
admin.site.register(Currency)
admin.site.register(CompanySetting)
