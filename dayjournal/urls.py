from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.day_journal, name='new_day_journal'),
                       url(r'^(?P<id>[0-9]+)/$', views.day_journal, name='view_day_journal'),
                       url(r'^save/cash_sales/$', views.save_cash_sales, name='save_cash_sales'),
                       url(r'^save/cash_purchase/$', views.save_cash_purchase, name='save_cash_purchase'),
                       url(r'^save/cash_receipt/$', views.save_cash_receipt, name='save_cash_receipt'),
                       url(r'^save/cash_payment/$', views.save_cash_payment, name='save_cash_payment'),
                       url(r'^save/credit_sales/$', views.save_credit_sales, name='save_credit_sales'),
                       url(r'^save/credit_purchase/$', views.save_credit_purchase, name='save_credit_purchase'),
                       url(r'^save/credit_expense/$', views.save_credit_expense, name='save_credit_expense'),
                       url(r'^save/credit_income/$', views.save_credit_income, name='save_credit_income'),
                       url(r'^save/summary_cash_and_equivalent/$', views.save_summary_cash_and_equivalent,
                           name='save_summary_cash_and_equivalent'),
                       # url(r'^day/save/(?P<submodel>[a-zA-Z0-9_.-]+)/$', views.save_submodel, name='save_submodel'),
)

