import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from payroll.models import Entry, EntryRow
from payroll.serializers import EntrySerializer
from acubor.lib import save_model, invalid
from ledger.models import delete_rows


@login_required
def entry(request, id=None):
    if id:
        entry = get_object_or_404(Entry, id=id, company=request.user.company)
        scenario = 'Update'
    else:
        entry = Entry()
        scenario = 'Create'
    data = EntrySerializer(entry).data
    return render(request, 'entry.html', {'data': data, 'scenario': scenario})


@login_required
def list_payroll_entries(request):
    objects = Entry.objects.filter(company=request.user.company)
    return render(request, 'list_all_entries.html', {'objects': objects})


@login_required
def delete_payroll_entry(request, id):
    object = get_object_or_404(Entry, id=id, company=request.user.company)
    object.delete()
    return redirect('/payroll/entries/')


@login_required
def save_entry(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    values = {
        'company': request.user.company, 'entry_no': params.get('entry_no')
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
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['pay_heading', 'account_id', 'amount', 'tax']):
            continue
        values = {'sn': index + 1, 'employee_id': row.get('account_id'), 'pay_heading_id': row.get('pay_heading'),
                  'tax': row.get('tax'), 'remarks': row.get('remarks'), 'hours': row.get('hours'),
                  'amount': row.get('amount'), 'entry': entry}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)

    return HttpResponse(json.dumps(dct), mimetype="application/json")