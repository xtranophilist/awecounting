from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^accounts/$', views.list_bank_accounts, name='list_bank_accounts'),
                       url(r'^cheque-deposits/$', views.list_cheque_deposits, name='list_cheque_deposits'),
                       url(r'^cash-deposits/$', views.list_cash_deposits, name='list_cash_deposits'),
                       url(r'^cheque-payments/$', views.list_cheque_payments, name='list_cheque_payments'),
                       url(r'^account/create/$', views.bank_account_form, name='create_bank_account'),
                       url(r'^account/update/(?P<id>[0-9]+)$', views.bank_account_form, name='update_bank_account'),
                       url(r'^cheque-deposit/$', views.cheque_deposit, name='new_cheque_deposit'),
                       url(r'^cheque-deposit/(?P<id>[0-9]+)$', views.cheque_deposit, name='update_cheque_deposit'),
                       url(r'^cash-deposit/$', views.cash_deposit, name='new_cash_deposit'),
                       url(r'^cash-deposit/(?P<id>[0-9]+)$', views.cash_deposit, name='update_cash_deposit'),
                       url(r'^cheque-payment/$', views.cheque_payment, name='new_cheque_payment'),
                       url(r'^cheque-payment/(?P<id>[0-9]+)$', views.cheque_payment, name='update_cheque_payment'),
)

