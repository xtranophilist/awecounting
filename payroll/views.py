import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from payroll.models import Entry, EntryRow
from payroll.serializers import EntrySerializer
from acubor.lib import save_model, invalid
from ledger.models import delete_rows, set_transactions, Account


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
    print params
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