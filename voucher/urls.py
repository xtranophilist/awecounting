from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^invoices/$', views.list_invoice, name='list_invoice'),
                       url(r'^invoice/new$', views.invoice, name='new_invoice'),
                       url(r'^invoice/(?P<id>[0-9]+)/$', views.invoice, name='view_invoice'),
                       url(r'^invoice/save/$', views.save_invoice, name='save_invoice'),
                       url(r'^purchase/$', views.purchase_voucher, name='purchase_voucher'),
                       url(r'^purchase/(?P<id>[0-9]+)/$', views.purchase_voucher, name='purchase_view'),
                       )
