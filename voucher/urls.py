from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^invoices/$', views.all_invoices, name='all_invoices'),
                       url(r'^invoice/new/$', views.invoice, name='new_invoice'),
                       url(r'^invoice/(?P<invoice_no>[0-9]+)/$', views.invoice, name='view_invoice'),
                       url(r'^invoice/(?P<invoice_no>[0-9]+)/delete/$', views.delete_invoice, name='delete_invoice'),
                       url(r'^invoice/save/$', views.save_invoice, name='save_invoice'),
                       url(r'^invoice/save_and_continue/$', views.save_invoice_and_continue,
                           name='save_invoice_and_continue'),
                       url(r'^invoice/approve/$', views.approve_invoice, name='approve_invoice'),
                       url(r'^invoice/cancel/$', views.cancel_invoice, name='cancel_invoice'),


                       url(r'^purchases/$', views.all_purchase_vouchers, name='all_purchase_vouchers'),
                       url(r'^purchase/new/$', views.purchase_voucher, name='new_purchase_voucher'),
                       url(r'^purchase/(?P<id>[0-9]+)/$', views.purchase_voucher, name='view_purchase_voucher'),
                       url(r'^journals/$', views.list_journal_vouchers, name='list_journal_vouchers'),
                       url(r'^journal/$', views.journal_voucher, name='new_journal_voucher'),
                       url(r'^journal/(?P<id>[0-9]+)/$', views.journal_voucher, name='update_journal_voucher'),
                       url(r'^journal/save/$', views.save_journal_voucher, name='save_journal_voucher'),


                       url(r'^purchase/(?P<id>[0-9]+)/delete/$', views.delete_purchase_voucher,
                           name='delete_purchase_voucher'),
                       url(r'^journal/(?P<id>[0-9]+)/delete/$', views.delete_journal_voucher,
                           name='delete_journal_voucher'),

                       url(r'^cash-receipts/$', views.list_cash_receipts, name='list_cash_receipts'),
                       url(r'^cash-receipt/$', views.cash_receipt, name='create_cash_receipt'),
                       url(r'^cash-receipt/(?P<id>[0-9]+)/$', views.cash_receipt, name='update_cash_receipt'),
)
