from django.contrib import admin
from models import Account, InventoryAccount, Tag, Transaction

admin.site.register(Account)
admin.site.register(InventoryAccount)
admin.site.register(Tag)
admin.site.register(Transaction)