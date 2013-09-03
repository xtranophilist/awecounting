from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       # url(r'^accounts/$', views.bank_accounts, name='list_bank_accounts'),
                       url(r'^account/create/$', views.bank_account_form, name='create_bank_account'),
                       url(r'^cheque-deposit/$', views.cheque_deposit, name='new_cheque_deposit'),
                       url(r'^cheque-deposit/(?P<id>[0-9]+)$', views.cheque_deposit, name='view_cheque_deposit'),
                       url(r'^cash-deposit/$', views.cash_deposit, name='new_cash_deposit'),
                       url(r'^cash-deposit/(?P<id>[0-9]+)$', views.cash_deposit, name='view_cash_deposit'),
                       url(r'^cheque-payment/$', views.cheque_payment, name='new_cheque_payment'),
                       url(r'^cheque-payment/(?P<id>[0-9]+)$', views.cheque_payment, name='view_cheque_payment'),
)

