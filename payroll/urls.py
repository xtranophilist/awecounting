from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^entry/$', views.entry, name='create_payroll_entry'),
                       url(r'^entries/$', views.list_payroll_entries, name='list_payroll_entries'),
                       url(r'^(?P<id>[0-9]+)/$', views.entry, name='update_payroll_entry'),
                       url(r'^entry/delete/(?P<id>[0-9]+)/$', views.delete_payroll_entry, name='delete_payroll_entry'),

                       url(r'^save/$', views.save_entry, name='save_payroll_entry'),

                       url(r'^employee/create/$', views.employee_form, name='create_employee'),
                       url(r'^employee/(?P<id>[0-9]+)/$', views.employee_form, name='update_employee'),
                       url(r'^employees/$', views.list_employees, name='list_employees'),
                       url(r'^employee/delete/(?P<id>[0-9]+)/$', views.delete_employee, name='delete_employee'),
                       url(r'^employees.json$', views.employees_as_json, name='employees_as_json'),

                       url(r'^day-attendance-voucher/$', views.attendance_voucher, name='create_attendance_voucher'),
                       url(r'^day-attendance-voucher/save/$', views.save_attendance_voucher,
                           name='save_attendance_voucher'),
                       url(r'^day-attendance-voucher/delete/(?P<id>[0-9]+)/$', views.delete_attendance_voucher,
                           name='delete_attendance_voucher'),
                       url(r'^day-attendance-voucher/(?P<id>[0-9]+)/$', views.attendance_voucher,
                           name='update_attendance_voucher'),

                       url(r'^attendance-voucher/$', views.work_time_voucher, name='create_work_time_voucher'),
                       url(r'^attendance-voucher/save/$', views.save_work_time_voucher,
                           name='save_work_time_voucher'),
                       url(r'^attendance-voucher/delete/(?P<id>[0-9]+)/$', views.delete_work_time_voucher,
                           name='delete_work_time_voucher'),
                       url(r'^attendance-voucher/(?P<id>[0-9]+)/$', views.work_time_voucher,
                           name='update_work_time_voucher'),

                       url(r'^group-voucher/$', views.group_payroll_voucher, name='create_group_payroll_voucher'),
                       url(r'^group-voucher/(?P<id>[0-9]+)/$', views.group_payroll_voucher,
                           name='update_group_payroll_voucher'),
                       url(r'^group-voucher/save/$', views.save_group_payroll_voucher,
                           name='save_group_payroll_voucher'),
                       url(r'^group-voucher/approve/$', views.approve_group_payroll_voucher,
                           name='approve_group_payroll_voucher'),
                       url(r'^group-voucher/delete/(?P<id>[0-9]+)/$', views.delete_group_payroll_voucher,
                           name='delete_group_payroll_voucher'),

                       url(r'^individual-voucher/$', views.individual_payroll_voucher, name='create_individual_payroll_voucher'),
                       url(r'^individual-voucher/(?P<id>[0-9]+)/$', views.individual_payroll_voucher,
                           name='update_individual_payroll_voucher'),
                       url(r'^individual-voucher/save/$', views.save_individual_payroll_voucher,
                           name='save_individual_payroll_voucher'),
                       url(r'^individual-voucher/approve/$', views.approve_individual_payroll_voucher,
                           name='approve_individual_payroll_voucher'),
                       url(r'^individual-voucher/delete/(?P<id>[0-9]+)/$', views.delete_individual_payroll_voucher,
                           name='delete_individual_payroll_voucher'),
)