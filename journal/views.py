from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from inventory.models import Item
from inventory.forms import ItemForm
from journal.models import DayCashPayment, DayCashReceipt, DayCashSales, DayCashPurchase, DayCreditExpense, \
    DayCreditIncome, DayCreditPurchase, DayCreditSales, DayPayroll, DaySummaryBank, DaySummaryCash, \
    DaySummaryEquivalent, DaySummaryInventory, DaySummarySalesTax


def day_journal(request, id=None):
    if id:
        day_journal = get_object_or_404(Item, id=id)
    else:
        item = Item()
    if request.POST:
        form = ItemForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.company
            item.save()
    else:
        form = ItemForm(instance=item)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'item_form.html', {
        'form': form,
        'base_template': base_template,
    })
