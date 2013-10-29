from datetime import date
import json
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from payroll.models import Entry, EntryRow, Employee, AttendanceVoucher, WorkTimeVoucher
from payroll.serializers import EntrySerializer, AttendanceVoucherSerializer, EmployeeSerializer, WorkTimeVoucherSerializer
from acubor.lib import save_model, invalid
from ledger.models import delete_rows, set_transactions, Account
from payroll.forms import EmployeeForm


@login_required
def entry(request, id=None):
    if id:
        entry = get_object_or_404(Entry, id=id, company=request.company)
        scenario = 'Update'
    else:
        entry = Entry()
        scenario = 'Create'
    data = EntrySerializer(entry).data
    return render(request, 'entry.html', {'data': data, 'scenario': scenario})


@login_required
def list_payroll_entries(request):
    objects = Entry.objects.filter(company=request.company)
    return render(request, 'list_all_entries.html', {'objects': objects})


@login_required
def delete_payroll_entry(request, id):
    object = get_object_or_404(Entry, id=id, company=request.company)
    object.delete()
    return redirect('/payroll/entries/')


@login_required
def save_entry(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    values = {
        'company': request.company, 'entry_no': params.get('entry_no')
    }
    if params.get('id'):
        entry = Entry.objects.get(id=params.get('id'))
    else:
        entry = Entry()
        # if not created:
    if params.get('rows') != [{}] or params.get('deleted_rows') != []:
        entry = save_model(entry, values)
        dct['id'] = entry.id
    model = EntryRow
    payroll_tax_account = Account.objects.get(name='Payroll Tax', company=request.company)
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['pay_heading', 'account_id', 'amount']):
            continue
        if row.get('tax') == '':
            row['tax'] = 0
        values = {'sn': index + 1, 'employee_id': row.get('account_id'), 'pay_heading_id': row.get('pay_heading'),
                  'tax': row.get('tax'), 'remarks': row.get('remarks'), 'hours': row.get('hours'),
                  'amount': row.get('amount'), 'entry': entry}
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
            #if request.is_ajax():
            #    return render(request, 'callback.html', {'obj': TaxSchemeSerializer(obj).data})
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
        voucher = WorkTimeVoucher.objects.get(id=params.get('id'))
    else:
        voucher = AttendanceVoucher()
    voucher = save_model(voucher, values)
    voucher.save()
    dct['id'] = voucher.id
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_attendance_voucher'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_work_time_voucher(request, id):
    obj = get_object_or_404(AttendanceVoucher, id=id, company=request.company)
    obj.delete()
    return redirect(reverse_lazy('list_attendance_voucher'))