from datetime import date, datetime
import json
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from payroll.models import Entry, EntryRow, Employee, AttendanceVoucher, WorkTimeVoucher, WorkTimeVoucherRow, WorkDay, GroupPayroll, GroupPayrollRow, IndividualPayroll, Inclusion, Deduction
from payroll.serializers import EntrySerializer, AttendanceVoucherSerializer, EmployeeSerializer, WorkTimeVoucherSerializer, GroupPayrollSerializer, IndividualPayrollSerializer
from acubor.lib import save_model, invalid, empty_to_zero
from ledger.models import delete_rows, set_transactions, Account, Category
from payroll.forms import EmployeeForm
from users.models import group_required


@login_required
def entry(request, id=None):
    if id:
        the_entry = get_object_or_404(Entry, id=id, company=request.company)
        scenario = 'Update'
    else:
        the_entry = Entry()
        scenario = 'Create'
    data = EntrySerializer(the_entry).data
    return render(request, 'entry.html', {'data': data, 'scenario': scenario})


@login_required
def list_payroll_entries(request):
    objects = Entry.objects.filter(company=request.company)
    return render(request, 'list_all_entries.html', {'objects': objects})


@login_required
def delete_payroll_entry(request, id):
    obj = get_object_or_404(Entry, id=id, company=request.company)
    obj.delete()
    return redirect('/payroll/entries/')


@login_required
def save_entry(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    values = {
        'company': request.company, 'entry_no': params.get('entry_no')
    }
    if params.get('id'):
        the_entry = Entry.objects.get(id=params.get('id'))
    else:
        the_entry = Entry()
        # if not created:
    if params.get('rows') != [{}] or params.get('deleted_rows') != []:
        the_entry = save_model(the_entry, values)
        dct['id'] = the_entry.id
    model = EntryRow
    payroll_tax_account = Account.objects.get(name='Payroll Tax', company=request.company)
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['pay_heading', 'account_id', 'amount']):
            continue
        if row.get('tax') == '':
            row['tax'] = 0
        values = {'sn': index + 1, 'employee_id': row.get('account_id'), 'pay_heading_id': row.get('pay_heading'),
                  'tax': row.get('tax'), 'remarks': row.get('remarks'), 'hours': row.get('hours'),
                  'amount': row.get('amount'), 'entry': the_entry}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        net_amount = float(row.get('amount')) - float(row.get('tax'))
        set_transactions(submodel, submodel.created,
                         ['dr', Account.objects.get(id=row.get('pay_heading'), company=request.company),
                          row.get('amount')],
                         ['cr', Account.objects.get(id=row.get('account_id'), company=request.company),
                          net_amount],
                         ['cr', payroll_tax_account, row.get('tax')],
        )
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)

    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def list_employees(request):
    pass


@login_required
def employee_form(request, id=None):
    if id:
        obj = get_object_or_404(Employee, id=id, company=request.company)
        scenario = 'Update'
    else:
        obj = Employee(company=request.company)
        scenario = 'Create'
    if request.POST:
        form = EmployeeForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = request.company
            obj.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': EmployeeSerializer(obj).data})
            return redirect(reverse_lazy('list_employees'))
    else:
        form = EmployeeForm(instance=obj)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'employee_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@login_required
def list_employees(request):
    objs = Employee.objects.filter(company=request.company)
    return render(request, 'list_employees.html', {'objects': objs})


@login_required
def employees_as_json(request):
    objs = Employee.objects.filter(company=request.company)
    objs_data = EmployeeSerializer(objs).data
    return HttpResponse(json.dumps(objs_data), mimetype="application/json")


@login_required
def delete_employee(request, id):
    obj = get_object_or_404(Employee, id=id, company=request.company)
    obj.delete()
    return redirect(reverse_lazy('list_employees'))


@login_required
def attendance_voucher(request, id=None):
    if id:
        voucher = get_object_or_404(AttendanceVoucher, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = AttendanceVoucher(date=date.today())
        scenario = 'Create'
    data = AttendanceVoucherSerializer(voucher).data
    return render(request, 'attendance_voucher.html', {'scenario': scenario, 'data': data})


@login_required
def save_attendance_voucher(request):
    params = json.loads(request.body)
    dct = {}
    values = {
        'company': request.company, 'voucher_no': params.get('voucher_no'), 'date': params.get('date'),
        'employee_id': params.get('employee'), 'from_date': params.get('from_date'), 'to_date': params.get('to_date'),
        'total_working_days': params.get('total_working_days'), 'full_present_day': params.get('full_present_day'),
        'half_present_day': params.get('half_present_day'), 'half_multiplier': params.get('half_multiplier'),
        'early_late_attendance_day': params.get('early_late_attendance_day'),
        'early_late_multiplier': params.get('early_late_multiplier'), 'total_ot_hours': params.get('total_ot_hours'),
        'paid': False
    }
    if params.get('id'):
        voucher = AttendanceVoucher.objects.get(id=params.get('id'))
    else:
        voucher = AttendanceVoucher()
    voucher = save_model(voucher, values)
    voucher.save()
    dct['id'] = voucher.id
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_attendance_voucher'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_attendance_voucher(request, id):
    obj = get_object_or_404(AttendanceVoucher, id=id, company=request.company)
    obj.delete()
    return redirect(reverse_lazy('list_attendance_voucher'))


@login_required
def work_time_voucher(request, id=None):
    if id:
        voucher = get_object_or_404(WorkTimeVoucher, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = WorkTimeVoucher(date=date.today())
        scenario = 'Create'
    data = WorkTimeVoucherSerializer(voucher).data
    return render(request, 'work_time_voucher.html', {'scenario': scenario, 'data': data})


@login_required
def save_work_time_voucher(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    values = {
        'company': request.company, 'voucher_no': params.get('voucher_no'), 'date': params.get('date'),
        'from_date': params.get('from_date'), 'to_date': params.get('to_date')}
    if params.get('id'):
        voucher = WorkTimeVoucher.objects.get(id=params.get('id'))
    else:
        voucher = WorkTimeVoucher()
    voucher = save_model(voucher, values)
    dct['id'] = voucher.id
    model = WorkTimeVoucherRow
    umodel = WorkDay
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['employee']):
            continue
        values = {'employee_id': row.get('employee'), 'work_time_voucher': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = {'id': submodel.id, 'days': {}}
        #deletion of work days not falling in range
        for work_day in submodel.work_days.all():
            from_date = datetime.strptime(params.get('from_date'), "%Y-%m-%d").date()
            to_date = datetime.strptime(params.get('to_date'), "%Y-%m-%d").date()
            if work_day.day < from_date or work_day.day > to_date:
                work_day.delete()
        for i, r in enumerate(row.get('work_days')):
            if invalid(r, ['in_time', 'out_time']):
                #submodel.delete()
                del dct['rows'][index]
                break
            values = {'in_time': r.get('in_time'), 'out_time': r.get('out_time'), 'day': r.get('day').get('yyyy_mm_dd'),
                      'work_time_voucher_row': submodel}
            try:
                ubersubmodel, created = umodel.objects.get_or_create(id=r.get('id'), defaults=values)
                if not created:
                    ubersubmodel = save_model(ubersubmodel, values)
            except Exception as e:
                #dct['error_message'] = str(e)
                #dct['culprit_row'] = index
                #dct['culprit_work_day'] = i
                del dct['rows'][index]
                break
            dct['rows'][index]['days'][i] = ubersubmodel.id
    delete_rows(params.get('deleted_rows'), model)
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_work_time_voucher'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_work_time_voucher(request, id):
    obj = get_object_or_404(AttendanceVoucher, id=id, company=request.company)
    obj.delete()
    return redirect(reverse_lazy('list_attendance_voucher'))


@login_required
def group_payroll_voucher(request, id=None):
    if id:
        voucher = get_object_or_404(GroupPayroll, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = GroupPayroll(date=date.today())
        scenario = 'Create'
    data = GroupPayrollSerializer(voucher).data
    return render(request, 'group_payroll_voucher.html', {'scenario': scenario, 'data': data})


@login_required
def save_group_payroll_voucher(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    voucher_values = {'date': params.get('date'), 'voucher_no': params.get('voucher_no'), 'company': request.company}
    if params.get('id'):
        voucher = GroupPayroll.objects.get(id=params.get('id'))
    else:
        voucher = GroupPayroll()
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = GroupPayrollRow
    for index, row in enumerate(params.get('table_vm').get('rows')):
        if invalid(row, ['employee', 'pay_head']):
            continue
        rate_day = empty_to_zero(row.get('rate_day'))
        rate_hour = empty_to_zero(row.get('rate_hour'))
        rate_ot_hour = empty_to_zero(row.get('rate_ot_hour'))
        values = {'employee_id': row.get('employee'), 'rate_day': rate_day,
                  'rate_hour': rate_hour, 'rate_ot_hour': rate_ot_hour,
                  'payroll_tax': row.get('payroll_tax'), 'pay_head_id': row.get('pay_head'),
                  'group_payroll': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('table_vm').get('deleted_rows'), model)
    voucher.status = 'Unapproved'
    voucher.save()
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_group_payroll_voucher'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_group_payroll_voucher(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = GroupPayroll.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    payroll_tax = Account.objects.get(name='Payroll Tax', company=request.company)
    for row in voucher.rows.all():
        amount = row.rate_day * row.employee.get_unpaid_days() + row.rate_hour * row.employee.get_unpaid_hours() + row.rate_ot_hour * row.employee.get_unpaid_ot_hours()
        net_amount = amount - row.payroll_tax
        set_transactions(row, voucher.date,
                         ['dr', row.pay_head, amount],
                         ['cr', payroll_tax, row.payroll_tax],
                         ['cr', row.employee.account, net_amount]
        )
        row.employee.set_paid()
    voucher.status = 'Approved'
    voucher.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_group_payroll_voucher(request, id):
    obj = get_object_or_404(GroupPayroll, id=id, company=request.company)
    obj.delete()
    return redirect(reverse_lazy('list_group_payroll_voucher'))


@login_required
def individual_payroll_voucher(request, id=None):
    if id:
        voucher = get_object_or_404(IndividualPayroll, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = IndividualPayroll(date=date.today())
        scenario = 'Create'
    data = IndividualPayrollSerializer(voucher).data
    employee_deductions = Category.objects.get(name='Employee Deductions', company=request.company)
    pay_head = Category.objects.get(name='Pay Head', company=request.company)
    return render(request, 'individual_payroll_voucher.html', {'scenario': scenario, 'data': data, 'employee_deductions': employee_deductions, 'pay_head': pay_head})


@login_required
def save_individual_payroll_voucher(request):
    params = json.loads(request.body)
    dct = {'rows1': {}, 'rows2': {}}
    voucher_values = {'date': params.get('date'), 'voucher_no': params.get('voucher_no'),
                      'employee_id': params.get('employee'), 'company': request.company, }
    if params.get('id'):
        voucher = IndividualPayroll.objects.get(id=params.get('id'))
    else:
        voucher = IndividualPayroll()
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = Inclusion
    for index, row in enumerate(params.get('inclusions').get('rows')):
        if invalid(row, ['account', 'amount']):
            continue
        values = {'particular_id': row.get('account'), 'amount': row.get('amount'), 'individual_payroll': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows1'][index] = submodel.id
    delete_rows(params.get('inclusions').get('deleted_rows'), model)
    model = Deduction
    for index, row in enumerate(params.get('deductions').get('rows')):
        if invalid(row, ['account', 'amount']):
            continue
        values = {'particular_id': row.get('account'), 'amount': row.get('amount'), 'individual_payroll': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows2'][index] = submodel.id
    delete_rows(params.get('deductions').get('deleted_rows'), model)
    voucher.status = 'Unapproved'
    voucher.save()
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_individual_payroll_voucher'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_individual_payroll_voucher(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = IndividualPayroll.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")

    total_inclusion = 0
    for row in voucher.inclusions.all():
        set_transactions(row, voucher.date,
                         ['dr', row.particular, row.amount]
        )
        total_inclusion += row.amount

    total_exclusion = 0
    for row in voucher.deductions.all():
        set_transactions(row, voucher.date,
                         ['cr', row.particular, row.amount]
        )
        total_exclusion += row.amount

    diff = total_inclusion - total_exclusion

    if diff > 0:
        set_transactions(voucher, voucher.date,
                         ['cr', voucher.employee.account, diff]
        )
    elif diff < 0:
        set_transactions(voucher, voucher.date,
                         ['dr', voucher.employee.account, diff * (-1)]
        )
    voucher.employee.set_paid()
    voucher.status = 'Approved'
    voucher.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_individual_payroll_voucher(request, id):
    obj = get_object_or_404(GroupPayroll, id=id, company=request.company)
    obj.delete()
    return redirect(reverse_lazy('list_group_payroll_voucher'))
