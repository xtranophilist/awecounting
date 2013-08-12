from django.shortcuts import render, get_object_or_404
from daybook.models import DayBook, CashPayment, CashSales, CashPurchase, CashReceipt
from datetime import date
from daybook.serializers import DayBookSerializer
from django.http import HttpResponse
import json
from acubor.lib import delete_rows, invalid, save_model


def day_book(request, id=None):
    day_book, created = DayBook.objects.get_or_create(date=date.today(), company=request.user.company)
    day_book_data = DayBookSerializer(day_book).data
    base_template = 'dashboard.html'
    return render(request, 'day_book.html', {
        'day_book': day_book_data,
        'base_template': base_template,
        })


def get_book(request):
    book, created = DayBook.objects.get_or_create(date=json.loads(request.body).get('day_book_date'),
                                                        company=request.user.company)
    if created:
        book.save()
    return book


def save_cash_sales(request):
    params = json.loads(request.body)
    dct = {}
    model = CashSales
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['sales_ledger', 'amount']):
            continue
        values = {'sn': index+1, 'sales_ledger_id': row.get('sales_ledger'), 'amount': row.get('amount'),
                  'day_book': get_book(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct[index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_purchase(request):
    params = json.loads(request.body)
    dct = {}
    model = CashPurchase
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['item_id', 'amount', 'quantity']):
            continue
        values = {'sn': index+1, 'item_id': row.get('item_id'), 'amount': row.get('amount'),
                  'quantity': row.get('quantity'), 'day_book': get_book(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct[index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_receipt(request):
    params = json.loads(request.body)
    dct = {}
    model = CashReceipt
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['account_id', 'amount']):
            continue
        values = {'sn': index+1, 'account_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_book': get_book(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct[index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_cash_payment(request):
    params = json.loads(request.body)
    dct = {}
    model = CashPayment
    for index, row in enumerate(params.get('rows')):
        if invalid(row, ['account_id', 'amount']):
            continue
        values = {'sn': index+1, 'account_id': row.get('account_id'), 'amount': row.get('amount'),
                  'day_book': get_book(request)}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct[index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


def save_summary_cash(request):
    pass