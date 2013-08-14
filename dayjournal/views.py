from django.shortcuts import render, get_object_or_404
from dayjournal.models import DayJournal, CashPayment, CashSales, CashPurchase, CashReceipt, \
    CreditExpense, CreditIncome, CreditPurchase, CreditSales
from datetime import date
from dayjournal.serializers import DayJournalSerializer
from django.http import HttpResponse
import json
from acubor.lib import delete_rows, invalid, save_model


def day_journal(request, id=None):
    day_journal, created = DayJournal.objects.get_or_create(date=date.today(), company=request.user.company)
    day_journal_data = DayJournalSerializer(day_journal).data
    base_template = 'dashboard.html'
    return render(request, 'day_journal.html', {
        'day_journal': day_journal_data,
        'base_template': base_template,
        })


def get_journal(request):
    journal, created = DayJournal.objects.get_or_create(date=json.loads(request.body).get('day_journal_date'),
                                                        company=request.user.company)
    if created:
        journal.save()
    return journal


def save_cash_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashSales
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index+1, 'sales_ledger_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_purchase(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashPurchase
    for index, row in enumerate(params.get('rows')):
        print row
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index+1, 'purchase_ledger_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_payment(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashPayment
    for index, row in enumerate(params.get('rows')):
        print row
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index+1, 'payment_to_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_receipt(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashReceipt
    for index, row in enumerate(params.get('rows')):
        print row
        invalid_attrs = invalid(row, ['account_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index+1, 'received_from_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_credit_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CreditSales
    for index, row in enumerate(params.get('rows')):
        print row
        invalid_attrs = invalid(row, ['account_cr_id', 'account_dr_id', 'amount'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index+1, 'sales_ledger_id': row.get('account_cr_id'), 'customer_id': row.get('account_dr_id'),
                  'amount': row.get('amount'), 'day_journal': get_journal(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_credit_purchase(request):
    pass


def save_credit_income(request):
    pass


def save_credit_expense(request):
    pass


def save_summary_cash(request):
    pass