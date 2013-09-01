from django.shortcuts import render, redirect, get_object_or_404
from payroll.models import Entry, EntryRow
from payroll.serializers import EntrySerializer
import json
from acubor.lib import save_model, invalid
from ledger.models import delete_rows
from django.http import HttpResponse


def entry(request, id=None):
    if id:
        entry = get_object_or_404(Entry, id=id)
    else:
        entry = Entry()
        # form = InvoiceForm(data=request.POST, instance=invoice)
    data = EntrySerializer(entry).data
    return render(request, 'entry.html', {'data': data})


def save_entry(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    values = {
        'company': request.user.company
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