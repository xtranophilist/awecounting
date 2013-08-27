from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^account/new/$', views.bank_account_form, name='create_bank_account'),
                       url(r'^cheque-receipt/$', views.cheque_receipt, name='new_cheque_receipt'),
                       url(r'^cheque-receipt/(?P<id>[0-9]+)$', views.cheque_receipt, name='view_cheque_receipt'),
                       url(r'^cash-receipt/$', views.cash_receipt, name='new_cash_receipt'),
                       url(r'^cash-receipt/(?P<id>[0-9]+)$', views.cash_receipt, name='view_cash_receipt'),
)

