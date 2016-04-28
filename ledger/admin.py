from django.contrib import admin

from models import Account, Transaction, JournalEntry


class AccountAdmin(admin.ModelAdmin):
    # fields = ('name', 'current_cr', 'current_dr')
    list_display = ('name', 'current_cr', 'current_dr')


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
