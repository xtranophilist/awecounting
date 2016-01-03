from django.contrib import admin
from voucher.models import Invoice, PurchaseVoucher, JournalVoucher, CashReceipt

admin.site.register(Invoice)
admin.site.register(PurchaseVoucher)
admin.site.register(JournalVoucher)
admin.site.register(CashReceipt)
