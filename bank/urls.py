from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^account/new/$', views.bank_account_form, name='create_bank_account'),
                       url(r'^cheque-receipt/$', views.cheque_receipt, name='new_cheque_deposit'),
)

