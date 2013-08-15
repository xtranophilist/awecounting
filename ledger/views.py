from ledger.models import Account
from ledger.serializers import AccountSerializer
from django.http import HttpResponse
import json
from django.shortcuts import render, get_object_or_404
from forms import AccountForm


def accounts_as_json(request):
    accounts = Account.objects.all()
    items_data = AccountSerializer(accounts).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


def account_form(request, id=None):
    if id:
        account = get_object_or_404(Account, id=id)
    else:
        account = Account()
    if request.POST:
        form = AccountForm(data=request.POST, instance=account)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.company
            item.save()
    else:
        form = AccountForm(instance=account)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'account_form.html', {
        'form': form,
        'base_template': base_template,
    })