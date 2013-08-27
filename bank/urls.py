from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^account/new/$', views.bank_account_form, name='create_bank_account'),
                       url(r'^cheque-deposit/$', views.cheque_deposit, name='new_cheque_deposit'),
)

