from ledger.models import Account, JournalEntry, Category, Party
from ledger.serializers import AccountSerializer
from django.http import HttpResponse
import json
from django.shortcuts import render, get_object_or_404, redirect
from forms import AccountForm, CategoryForm, PartyForm


def accounts_as_json(request):
    accounts = Account.objects.filter(company=request.user.company)
    items_data = AccountSerializer(accounts).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


def accounts_by_day_as_json(request, day):
    accounts = Account.objects.filter(company=request.user.company)
    items_data = AccountSerializer(accounts, day=day).data
    # items_data = AccountSerializer(accounts).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


def account_form(request, id=None):
    if id:
        account = get_object_or_404(Account, id=id)
        scenario = 'Update'
    else:
        account = Account()
        scenario = 'Create'
    if request.POST:
        form = AccountForm(data=request.POST, instance=account, company=request.user.company)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.company
            item.save()
            form.save_m2m()
            return redirect('/ledger/')
    else:
        form = AccountForm(instance=account, company=request.user.company)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'account_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


def list_accounts(request):
    all_accounts = Account.objects.all()
    return render(request, 'list_accounts.html', {'accounts': all_accounts})


def view_account(request, id):
    account = get_object_or_404(Account, id=id)
    # transactions = account.transactions
    base_template = 'dashboard.html'
    journal_entries = JournalEntry.objects.filter(transactions__account_id=account.id).order_by('id',
                                                                                                'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    return render(request, 'view_account.html', {
        'account': account,
        # 'transactions': transactions.all(),
        'journal_entries': journal_entries,
        'base_template': base_template,
    })


def list_categories(request):
    categories = Category.objects.filter(company=request.user.company)
    return render(request, 'list_categories.html', {'categories': categories})


def create_category(request):
    category = Category()
    if request.POST:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user.company
            category.save()
            return redirect('/categories/')
    else:
        form = CategoryForm(instance=category)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'category_create_form.html', {
        'form': form,
        'base_template': base_template,
    })


def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.POST:
        form = CategoryForm(data=request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user.company
            category.save()
            return redirect('/categories/')
    else:
        form = CategoryForm(instance=category)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'category_update_form.html', {
        'form': form,
        'base_template': base_template
    })


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('/categories/')


def delete_account(request, id):
    object = get_object_or_404(Account, id=id)
    object.delete()
    return redirect('/ledger/')


def party_form(request, id=None):
    if id:
        party = get_object_or_404(Party, id=id)
    else:
        party = Party()
    if request.POST:
        form = PartyForm(data=request.POST, instance=party)
        if form.is_valid():
            party = form.save(commit=False)
            party.company = request.user.company
            party.save()
    else:
        form = PartyForm(instance=party)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'party_form.html', {
        'form': form,
        'base_template': base_template,
    })
