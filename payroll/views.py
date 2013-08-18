# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from payroll.models import Entry
from payroll.serializers import EntrySerializer


def entry(request, id=None):
    if id:
        entry = get_object_or_404(Entry, id=id)
    else:
        entry = Entry(company=request.user.company)
    # form = InvoiceForm(data=request.POST, instance=invoice)
    data = EntrySerializer(entry).data
    return render(request, 'entry.html', {'data': data})
