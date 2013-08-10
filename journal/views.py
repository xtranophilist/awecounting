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
    pass


# def save_day_cash_purchase(request):
#     params = json.loads(request.body)
#     required = ['item_id', 'amount']
#     day_journal = get_journal(request)
#     dct = {}
#     DayCashPurchase.objects.filter(day_journal=day_journal).delete()
#     for index, row in enumerate(params.get('rows')):
#         valid = True
#         for attr in required:
#             # if one of the required attributes isn't received or is an empty string
#             if not attr in row or row.get(attr) == "":
#                 valid = False
#         if not valid:
#             continue
#         day_cash_purchase = DayCashPurchase(sn=index + 1, item_id=row.get('item_id'), amount=row.get('amount'),
#                                             quantity=row.get('quantity'), day_journal=day_journal, id=row.get('id'))
#         day_cash_purchase.sn = index + 1
#         day_cash_purchase.item_id = row.get('item_id')
#         day_cash_purchase.amount = row.get('amount')
#         if row.get('quantity'):
#             day_cash_purchase.quantity = row.get('quantity')
#         day_cash_purchase.save()
#         dct[index] = day_cash_purchase.id
#     return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_day_cash_receipt(request):
    params = json.loads(request.body)
    required = ['account_id', 'amount']
    day_journal = get_journal(request)
    dct = {}
    DayCashReceipt.objects.filter(day_journal=day_journal).delete()
    for index, row in enumerate(params.get('rows')):
        valid = True
        for attr in required:
            # if one of the required attributes isn't received or is an empty string
            if not attr in row or row.get(attr) == "":
                valid = False
        if not valid:
            continue
        day_cash_receipt = DayCashReceipt(sn=index + 1, account_id=row.get('account_id'), amount=row.get('amount'),
                                          day_journal=day_journal, id=row.get('id'))
        day_cash_receipt.sn = index + 1
        day_cash_receipt.account_id = row.get('account_id')
        day_cash_receipt.amount = row.get('amount')
        day_cash_receipt.save()
        dct[index] = day_cash_receipt.id
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_day_cash_payment(request):
    params = json.loads(request.body)
    required = ['account_id', 'amount']
    day_journal = get_journal(request)
    dct = {}
    DayCashPayment.objects.filter(day_journal=day_journal).delete()
    for index, row in enumerate(params.get('rows')):
        valid = True
        for attr in required:
            # if one of the required attributes isn't received or is an empty string
            if not attr in row or row.get(attr) == "":
                valid = False
        if not valid:
            continue
        day_cash_payment = DayCashPayment(sn=index + 1, account_id=row.get('account_id'), amount=row.get('amount'),
                                          day_journal=day_journal, id=row.get('id'))
        day_cash_payment.sn = index + 1
        day_cash_payment.account_id = row.get('account_id')
        day_cash_payment.amount = row.get('amount')
        day_cash_payment.save()
        dct[index] = day_cash_payment.id
    return HttpResponse(json.dumps(dct), mimetype="application/json")