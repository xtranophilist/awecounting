from django.shortcuts import render, get_object_or_404
from journal.models import DayJournal, DayCashPayment, DayCashSales
from datetime import date
from journal.serializers import DayJournalSerializer
from django.http import HttpResponse
import json


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


def save_submodel(request, submodel):
    params = json.loads(request.body)
    required = ['item_id', 'amount']
    day_journal = get_journal(request)
    dct = {}
    for index, row in enumerate(params.get('rows')):
        print row
        valid = True
        for attr in required:
            # if one of the required attributes isn't received or is an empty string
            if not attr in row or row.get(attr) == "":
                valid = False
        if not valid:
            continue
        if not 'id' in row:
            day_cash_sales = DayCashSales(sn=index + 1, item_id=row.get('item_id'), amount=row.get('amount'),
                                          quantity=row.get('quantity'), day_journal=day_journal)
        else:
            day_cash_sales = DayCashSales.objects.get(id=row['id'])
        print row
        day_cash_sales.sn = index + 1
        day_cash_sales.item_id = row.get('item_id')
        day_cash_sales.amount = row.get('amount')
        day_cash_sales.quantity = row.get('quantity')
        day_cash_sales.save()
        dct[index] = day_cash_sales.id
    return HttpResponse(json.dumps(dct), mimetype="application/json")