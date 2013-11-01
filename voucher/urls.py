from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^invoices/$', views.all_invoices, name='all_invoices'),
                       url(r'^invoice/new/$', views.invoice, name='new_invoice'),
                       url(r'^invoice/(?P<invoice_no>[0-9]+)/$', views.invoice, name='view_invoice'),
                       url(r'^invoice/party/(?P<id>[0-9]+).json$', views.party_invoices, name='party_invoices'),
                       url(r'^invoice/(?P<invoice_no>[0-9]+)/delete/$', views.delete_invoice, name='delete_invoice'),
                       url(r'^invoice/save/$', views.save_invoice, name='save_invoice'),
                       url(r'^invoice/approve/$', views.approve_invoice, name='approve_invoice'),
                       url(r'^invoice/cancel/$', views.cancel_invoice, name='cancel_invoice'),


                       url(r'^purchases/$', views.all_purchase_vouchers, name='all_purchase_vouchers'),
                       url(r'^purchase/new/$', views.purchase_voucher, name='new_purchase_voucher'),
                       url(r'^purchase/(?P<id>[0-9]+)/$', views.purchase_voucher, name='view_purchase_voucher'),
                       url(r'^purchase/party/(?P<id>[0-9]+).json$', views.party_purchase_vouchers,
                           name='party_purchase_vouchers'),
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
                       url(r'^cash-receipt/save/$', views.save_cash_receipt, name='save_cash_receipt'),
                       url(r'^cash-receipt/approve/$', views.approve_cash_receipt, name='approve_cash_receipt'),

                       url(r'^cash-payments/$', views.list_cash_payments, name='list_cash_payments'),
                       url(r'^cash-payment/$', views.cash_payment, name='create_cash_payment'),
                       url(r'^cash-payment/(?P<id>[0-9]+)/$', views.cash_payment, name='update_cash_payment'),
                       url(r'^cash-payment/save/$', views.save_cash_payment, name='save_cash_payment'),
                       url(r'^cash-payment/approve/$', views.approve_cash_payment, name='approve_cash_payment'),

                       url(r'^fixed-assets/$', views.list_fixed_assets, name='list_fixed_assets'),
                       url(r'^fixed-asset/$', views.fixed_asset, name='create_fixed_asset'),
                       url(r'^fixed-asset/(?P<id>[0-9]+)/$', views.fixed_asset, name='update_fixed_asset'),
                       url(r'^fixed-asset/save/$', views.save_fixed_asset, name='save_fixed_asset'),
                       url(r'^fixed-asset/approve/$', views.approve_fixed_asset, name='approve_fixed_asset'),


)
