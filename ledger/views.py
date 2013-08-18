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


def accounts_by_day_as_json(request, day):
    accounts = Account.objects.all()
    print 'twat'
    items_data = AccountSerializer(accounts, day=day).data
    print 'fat'
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


def list_accounts(request):
    all_accounts = Account.objects.all()
    return render(request, 'list_accounts.html', {'accounts': all_accounts})


def view_account(request, id):
    account = get_object_or_404(Account, id=id)
    transactions = account.transactions
    base_template = 'dashboard.html'
    return render(request, 'view_account.html', {
        'account': account,
        'transactions': transactions.all(),
        'base_template': base_template,
    })