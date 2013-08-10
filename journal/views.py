from django.shortcuts import render, get_object_or_404
from journal.models import DayJournal, DayCashPayment, DayCashSales, DayCashPurchase, DayCashReceipt
from datetime import date
from journal.serializers import DayJournalSerializer
from django.http import HttpResponse
import json
from acubor.lib import delete_rows, invalid, save_model


def day_journal(request, id=None):
    day_journal, created = DayJournal.objects.get_or_create(date=date.today(), company=request.user.company)
    day_journal_data = DayJournalSerializer(day_journal).data
    base_template = 'dashboard.html'
    return render(request, 'day_journal.html', {
        'journal': day_journal_data,
        'base_template': base_template,
        })


def get_journal(request):
    journal, created = DayJournal.objects.get_or_create(date=json.loads(request.body).get('journal_date'),
                                                        company=request.user.company)
    if created:
        journal.save()
    return journal


def save_day_cash_sales(request):
    params = json.loads(request.body)
    dct = {}
    model = DayCashSales
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['item_id', 'amount', 'quantity']):
            continue
        values = {'sn': index+1, 'item_id': row.get('item_id'), 'amount': row.get('amount'),
                  'quantity': row.get('quantity'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct[index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_day_cash_purchase(request):
    params = json.loads(request.body)
    dct = {}
    model = DayCashPurchase
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['item_id', 'amount', 'quantity']):
            continue
        values = {'sn': index+1, 'item_id': row.get('item_id'), 'amount': row.get('amount'),
                  'quantity': row.get('quantity'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct[index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_day_cash_receipt(request):
    params = json.loads(request.body)
    dct = {}
    model = DayCashReceipt
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['account_id', 'amount']):
            continue
        values = {'sn': index+1, 'account_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct[index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_day_cash_payment(request):
    params = json.loads(request.body)
    dct = {}
    model = DayCashPayment
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['account_id', 'amount']):
            continue
        values = {'sn': index+1, 'account_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct[index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_day_summary_cash(request):
    pass