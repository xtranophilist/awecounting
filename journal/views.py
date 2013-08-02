from django.shortcuts import render, get_object_or_404
from journal.models import DayJournal, DayCashPayment
from datetime import date


def day_journal(request, id=None):
    day_journal = DayJournal(date=date.today(), company=request.user.company)
    base_template = 'dashboard.html'

    return render(request, 'day_journal.html', {
        'journal': day_journal,
        'base_template': base_template,
    })
