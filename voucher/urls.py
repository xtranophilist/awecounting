from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^invoice/$', views.invoice, name='invoice'),
                       url(r'^invoice/(?P<id>[0-9]+)/$', views.invoice, name='invoice_view'),
                       url(r'^purchase/$', views.purchase_voucher, name='purchase_voucher'),
                       url(r'^purchase/(?P<id>[0-9]+)/$', views.purchase_voucher, name='purchase_view'),
                       url(r'^invoice/save/$', views.save_invoice, name='save_invoice')
)
