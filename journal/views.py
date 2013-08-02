from django.shortcuts import render, get_object_or_404
from journal.models import DayJournal, DayCashPayment
from datetime import date
from journal.serializers import DayJournalSerializer


def day_journal(request, id=None):
    day_journal = DayJournal(date=date.today(), company=request.user.company)
    day_journal_data = DayJournalSerializer(day_journal).data
    base_template = 'dashboard.html'
    return render(request, 'day_journal.html', {
        'journal_data': day_journal_data,
        'base_template': base_template,
    })
