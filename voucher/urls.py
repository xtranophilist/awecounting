from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^invoices/$', views.list_invoice, name='list_invoice'),
                       url(r'^invoice/new$', views.invoice, name='new_invoice'),
                       url(r'^invoice/(?P<invoice_no>[0-9]+)/$', views.invoice, name='view_invoice'),
                       url(r'^invoice/save/$', views.save_invoice, name='save_invoice'),
                       url(r'^purchase/$', views.purchase_voucher, name='new_purchase_voucher'),
                       url(r'^journal/$', views.journal_voucher, name='new_journal_voucher'),
                       url(r'^journal/(?P<id>[0-9]+)/$', views.journal_voucher, name='view_journal_voucher'),
                       url(r'^journal/save$', views.save_journal_voucher, name='save_journal_voucher'),
                       url(r'^bank/$', views.bank_voucher, name='new_bank_voucher'),
                       url(r'^bank/(?P<id>[0-9]+)/$', views.bank_voucher, name='view_bank_voucher'),
                       url(r'^bank/save$', views.save_bank_voucher, name='save_bank_voucher'),
                       )
