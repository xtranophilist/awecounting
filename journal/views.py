from django.shortcuts import render, get_object_or_404
from journal.models import DayJournal, DayCashPayment
from datetime import date
from journal.serializers import DayJournalSerializer
from django.http import HttpResponse
import json


def day_journal(request, id=None):
    day_journal = DayJournal(date=date.today(), company=request.user.company)
    day_journal_data = DayJournalSerializer(day_journal).data
    base_template = 'dashboard.html'
    return render(request, 'day_journal.html', {
        'journal': day_journal_data,
        'base_template': base_template,
    })


def save_journal_if_not_exist(date, company):
    journal, created = DayJournal.objects.get_or_create(date=date, company=company)
    if created:
        journal.save()
    return journal


def save_submodel(request, submodel):
    params = json.loads(request.body)
    required = params.get('required')
    for row in params.get('rows'):
        valid = True
        for attr in required:
            # if one of the required attributes isn't received
            if not attr in row:
                valid = False
            # if one of the required attributes is an empty string
            if row.get(attr) == "":
                valid = False
        if not valid:
            continue
        print row
    journal = save_journal_if_not_exist(params['journal_date'], request.user.company)
    return HttpResponse(json.dumps({}), mimetype="application/json")